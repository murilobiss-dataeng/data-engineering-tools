"""Enhanced Text-to-Speech - Prioridade: ElevenLabs (voz premium)."""

import os
import sys
import asyncio
import logging
import subprocess
import tempfile
from typing import Optional
from pydub import AudioSegment

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Piper TTS - gratuito, offline (pt_BR)
PIPER_PT_BR_MODEL = "pt_BR-faber-medium"

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# ElevenLabs - Vozes premium em português brasileiro
# Vozes recomendadas para conteúdo espiritual:
# - river: Voz masculina calma e serena (ideal para salmos)
# - eric: Voz masculina natural
# - rachel: Voz feminina suave
# - adam: Voz masculina profunda
ELEVENLABS_VOICES = {
    "river": "SAz9YHcvj6GT2YYXdXww",      # Masculina calma
    "eric": "cjVigY5qzO86Huf0OWal",        # Masculina natural
    "rachel": "21m00Tcm4TlvDq8ikWAM",      # Feminina suave
    "adam": "pNInz6obpgDQGcFmaJgB",        # Masculina profunda
    "josh": "TxGEqnHWrfWFTfGW9XjX",        # Masculina narrativa
    "arnold": "VR6AewLTigWG4xSOukaG",      # Masculina forte
    "bella": "EXAVITQu4vr4xnSDxMaL",       # Feminina expressiva
    "domi": "AZnzlk1XvdvUeBnXmlld",        # Feminina clara
}

# Configurações de qualidade ElevenLabs
ELEVENLABS_CONFIG = {
    "model_id": "eleven_multilingual_v2",  # Melhor modelo multilíngue
    "output_format": "mp3_44100_128",      # Boa qualidade: 44.1kHz, 128kbps (disponível no plano gratuito)
    "stability": 0.5,                       # Estabilidade da voz (0.0-1.0)
    "similarity_boost": 0.75,               # Similaridade com voz original
    "style": 0.0,                           # Estilo expressivo (0.0-1.0)
    "use_speaker_boost": True,              # Melhora qualidade do speaker
}

def _piper_available() -> bool:
    """Check if Piper binary is available."""
    try:
        result = subprocess.run(["piper", "--help"], capture_output=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


class EnhancedTextToSpeech:
    """TTS: ElevenLabs (humano) > edge-tts > Piper > gTTS."""

    def __init__(
        self,
        output_dir: str = "outputs",
        voice: str = "river",
        use_fallback: bool = True
    ):
        self.output_dir = output_dir
        self.voice = voice  # ElevenLabs: river, eric | edge-tts: pt-BR-FranciscaNeural
        self.use_fallback = use_fallback
        os.makedirs(output_dir, exist_ok=True)

    def _generate_elevenlabs(self, text: str, output_path: str) -> bool:
        """Gera áudio com ElevenLabs (voz premium de alta qualidade)."""
        key = os.getenv("ELEVENLABS_API_KEY")
        if not key:
            logger.warning("ELEVENLABS_API_KEY não configurada")
            return False
        try:
            from elevenlabs.client import ElevenLabs
            from elevenlabs import VoiceSettings
            
            client = ElevenLabs(api_key=key)
            voice_id = ELEVENLABS_VOICES.get(self.voice, ELEVENLABS_VOICES["river"])
            
            # Configurações de voz para qualidade premium
            voice_settings = VoiceSettings(
                stability=ELEVENLABS_CONFIG["stability"],
                similarity_boost=ELEVENLABS_CONFIG["similarity_boost"],
                style=ELEVENLABS_CONFIG["style"],
                use_speaker_boost=ELEVENLABS_CONFIG["use_speaker_boost"],
            )
            
            audio = client.text_to_speech.convert(
                voice_id=voice_id,
                text=text,
                model_id=ELEVENLABS_CONFIG["model_id"],
                output_format=ELEVENLABS_CONFIG["output_format"],
                voice_settings=voice_settings,
            )
            
            # Converte generator/iterator para bytes
            if isinstance(audio, bytes):
                data = audio
            elif hasattr(audio, "__iter__"):
                data = b"".join(chunk for chunk in audio)
            else:
                data = bytes(audio)
            
            with open(output_path, "wb") as f:
                f.write(data)
            
            logger.info(f"ElevenLabs: Áudio gerado com voz '{self.voice}' ({len(data)/1024:.1f} KB)")
            return True
            
        except ImportError:
            logger.warning("Pacote 'elevenlabs' não instalado. Execute: pip install elevenlabs")
            return False
        except Exception as e:
            logger.warning(f"ElevenLabs failed: {e}")
            return False

    def _generate_piper(self, text: str, output_path: str, _tried_download: bool = False) -> bool:
        """Gera áudio com Piper TTS (offline, gratuito)."""
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = tmp.name
            result = subprocess.run(
                [sys.executable, "-m", "piper", "-m", PIPER_PT_BR_MODEL, "-f", tmp_path, "--", text],
                capture_output=True,
                timeout=60,
                cwd=os.path.join(os.path.dirname(__file__), "..")
            )
            if result.returncode == 0 and os.path.exists(tmp_path):
                AudioSegment.from_wav(tmp_path).export(output_path, format="mp3", bitrate="192k")
                os.unlink(tmp_path)
                return True
            if not _tried_download and result.stderr and (b"not found" in result.stderr.lower() or result.returncode != 0):
                subprocess.run(
                    [sys.executable, "-m", "piper.download_voices", PIPER_PT_BR_MODEL],
                    capture_output=True,
                    timeout=120,
                    cwd=os.path.join(os.path.dirname(__file__), "..")
                )
                return self._generate_piper(text, output_path, _tried_download=True)
        except Exception as e:
            logger.debug(f"Piper failed: {e}")
        return False

    def _generate_edge_tts(self, text: str, output_path: str) -> bool:
        """Gera áudio com edge-tts."""
        if not EDGE_TTS_AVAILABLE:
            return False
        voice_name = self.voice if self.voice.startswith("pt-BR-") else "pt-BR-FranciscaNeural"
        try:
            communicate = edge_tts.Communicate(text=text, voice=voice_name)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(communicate.save(output_path))
            return True
        except Exception as e:
            logger.warning(f"edge-tts failed: {e}")
            return False

    def _generate_gtts(self, text: str, output_path: str) -> bool:
        """Gera áudio com gTTS (fallback)."""
        if not GTTS_AVAILABLE:
            return False
        try:
            tts = gTTS(text=text, lang='pt', slow=False, tld='com.br')
            tts.save(output_path)
            return True
        except Exception as e:
            logger.error(f"gTTS failed: {e}")
            return False

    def generate_audio(
        self,
        text: str,
        output_filename: Optional[str] = None,
        rate: str = "+0%",
        pitch: str = "+0Hz",
        force_elevenlabs: bool = True
    ) -> str:
        """Gera áudio com ElevenLabs (prioridade) ou fallbacks.
        
        Args:
            text: Texto para converter em áudio
            output_filename: Nome do arquivo de saída (opcional)
            rate: Taxa de fala (não usado com ElevenLabs)
            pitch: Tom da voz (não usado com ElevenLabs)
            force_elevenlabs: Se True, falha se ElevenLabs não disponível
            
        Returns:
            Caminho do arquivo de áudio gerado
        """
        import hashlib
        if output_filename is None:
            output_filename = f"tts_{hashlib.md5(text.encode()).hexdigest()}.mp3"
        output_path = os.path.join(self.output_dir, output_filename)

        # 1. ElevenLabs (PRIORIDADE - voz premium)
        if self._generate_elevenlabs(text, output_path):
            print(f"  ✓ Voz: ElevenLabs ({self.voice}) - Premium", flush=True)
            return output_path
        
        # Se force_elevenlabs e falhou, avisa mas continua com fallback
        if force_elevenlabs:
            print("  ⚠️ ElevenLabs não disponível. Configure ELEVENLABS_API_KEY.", flush=True)
            print("     Usando fallback...", flush=True)

        # 2. edge-tts (gratuito, qualidade OK)
        if self._generate_edge_tts(text, output_path):
            print("  ✓ Voz: edge-tts (Microsoft) - Gratuito", flush=True)
            return output_path

        # 3. Piper (gratuito, offline)
        if self._generate_piper(text, output_path):
            print("  ✓ Voz: Piper TTS - Gratuito/Offline", flush=True)
            return output_path

        # 4. gTTS (fallback básico)
        if self.use_fallback and self._generate_gtts(text, output_path):
            print("  ✓ Voz: gTTS (Google) - Básico", flush=True)
            return output_path

        raise RuntimeError(
            "Nenhum engine TTS disponível.\n"
            "Para voz premium, configure: ELEVENLABS_API_KEY=sua_chave\n"
            "Para fallback gratuito: pip install edge-tts gtts"
        )
    
    @staticmethod
    def check_elevenlabs_status() -> dict:
        """Verifica status da configuração do ElevenLabs."""
        key = os.getenv("ELEVENLABS_API_KEY")
        status = {
            "configured": bool(key),
            "key_preview": f"{key[:8]}...{key[-4:]}" if key and len(key) > 12 else None,
            "available_voices": list(ELEVENLABS_VOICES.keys()),
        }
        
        if key:
            try:
                from elevenlabs.client import ElevenLabs
                client = ElevenLabs(api_key=key)
                # Tenta obter informações da conta
                user = client.user.get()
                status["account_valid"] = True
                status["character_count"] = getattr(user, 'subscription', {}).get('character_count', 'N/A')
                status["character_limit"] = getattr(user, 'subscription', {}).get('character_limit', 'N/A')
            except Exception as e:
                status["account_valid"] = False
                status["error"] = str(e)
        
        return status

    def generate_audio_with_pauses(
        self,
        text: str,
        output_filename: Optional[str] = None,
        pause_duration: float = 0.6
    ) -> str:
        """Gera áudio com pausas entre frases."""
        import re
        sentences = re.split(r'[.!?]\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        audio_segments = []
        for i, sent in enumerate(sentences):
            try:
                seg_path = self.generate_audio(sent, output_filename=f"temp_sent_{i}.mp3")
                audio_segments.append(AudioSegment.from_mp3(seg_path))
                if os.path.exists(seg_path):
                    os.remove(seg_path)
                if i < len(sentences) - 1:
                    audio_segments.append(AudioSegment.silent(duration=int(pause_duration * 1000)))
            except Exception as e:
                logger.error(f"Erro na frase {i}: {e}")
        if not audio_segments:
            audio_segments = [AudioSegment.silent(duration=1000)]
        if output_filename is None:
            import hashlib
            output_filename = f"tts_{hashlib.md5(text.encode()).hexdigest()}.mp3"
        output_path = os.path.join(self.output_dir, output_filename)
        sum(audio_segments).export(output_path, format="mp3", bitrate="192k")
        return output_path
