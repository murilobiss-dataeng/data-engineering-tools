"""Enhanced Text-to-Speech with better quality for YouTube."""

import os
import asyncio
import logging
from typing import Optional
from pydub import AudioSegment

# Try to import edge_tts, fallback to gTTS if not available or fails
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

# Configure basic logging if not already configured
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnhancedTextToSpeech:
    """Generate high-quality speech audio using edge-tts with gTTS fallback."""
    
    # Brazilian Portuguese voices available in edge-tts
    BRAZILIAN_VOICES = [
        "pt-BR-FranciscaNeural",  # Female, natural
        "pt-BR-AntonioNeural",     # Male, natural
        "pt-BR-ThalitaNeural",     # Female, friendly
    ]
    
    def __init__(self, output_dir: str = "outputs", voice: str = None, use_fallback: bool = True):
        """Initialize enhanced TTS engine.
        
        Args:
            output_dir: Directory to save audio files
            voice: Voice name (default: FranciscaNeural for female)
            use_fallback: Whether to use gTTS as fallback if edge-tts fails
        """
        self.output_dir = output_dir
        self.voice = voice or self.BRAZILIAN_VOICES[0]  # FranciscaNeural
        self.use_fallback = use_fallback
        self._edge_tts_available = EDGE_TTS_AVAILABLE
        self._gtts_available = GTTS_AVAILABLE
        os.makedirs(output_dir, exist_ok=True)
    
    async def _generate_audio_async(
        self,
        text: str,
        output_path: str,
        rate: str = "+0%",
        pitch: str = "+0Hz"
    ) -> str:
        """Generate audio asynchronously using edge-tts.
        
        Args:
            text: Text to convert
            output_path: Output file path
            rate: Speech rate (e.g., "+0%", "+10%", "-10%")
            pitch: Pitch adjustment
            
        Returns:
            Path to generated audio
            
        Raises:
            Exception: If edge-tts fails
        """
        if not self._edge_tts_available:
            raise ImportError("edge-tts not available")
            
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=rate,
            pitch=pitch
        )
        await communicate.save(output_path)
        return output_path
    
    def _generate_audio_gtts_fallback(
        self,
        text: str,
        output_path: str
    ) -> str:
        """Generate audio using gTTS as fallback.
        
        Args:
            text: Text to convert
            output_path: Output file path
            
        Returns:
            Path to generated audio
        """
        if not self._gtts_available:
            raise ImportError("gTTS not available")
        
        # Use Brazilian Portuguese domain for better voice quality
        tts = gTTS(text=text, lang='pt', slow=False, tld='com.br')
        tts.save(output_path)
        return output_path
    
    def generate_audio(
        self,
        text: str,
        output_filename: Optional[str] = None,
        rate: str = "+0%",
        pitch: str = "+0Hz"
    ) -> str:
        """Generate audio file from text with automatic fallback.
        
        Args:
            text: Text to convert to speech
            output_filename: Optional output filename
            rate: Speech rate adjustment (only used with edge-tts)
            pitch: Pitch adjustment (only used with edge-tts)
            
        Returns:
            Path to generated audio file
        """
        if output_filename is None:
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()
            output_filename = f"tts_enhanced_{text_hash}.mp3"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Try edge-tts first if available
        if self._edge_tts_available:
            try:
                # Run async function - handle both new event loop and existing loop
                try:
                    # Try to get existing event loop
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # If loop is running, we need to use a different approach
                        import concurrent.futures
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(
                                lambda: asyncio.run(self._generate_audio_async(text, output_path, rate, pitch))
                            )
                            future.result(timeout=60)  # 60 second timeout
                    else:
                        # Loop exists but not running
                        loop.run_until_complete(self._generate_audio_async(text, output_path, rate, pitch))
                except RuntimeError:
                    # No event loop exists, create new one
                    asyncio.run(self._generate_audio_async(text, output_path, rate, pitch))
                
                logger.info(f"Successfully generated audio with edge-tts: {output_path}")
                return output_path
            except Exception as e:
                error_msg = f"edge-tts failed ({type(e).__name__}: {str(e)}), falling back to gTTS"
                logger.warning(error_msg)
                print(f"⚠️  {error_msg}")  # Also print to console for visibility
                if not self.use_fallback:
                    raise
        
        # Fallback to gTTS
        if self._gtts_available:
            try:
                self._generate_audio_gtts_fallback(text, output_path)
                logger.info(f"Successfully generated audio with gTTS: {output_path}")
                print(f"✅ Generated audio with gTTS: {output_path}")  # Console feedback
                return output_path
            except Exception as e:
                logger.error(f"gTTS also failed: {e}")
                raise RuntimeError(f"Both edge-tts and gTTS failed. Last error: {e}")
        else:
            raise RuntimeError("Neither edge-tts nor gTTS is available")
    
    def generate_audio_with_pauses(
        self,
        text: str,
        output_filename: Optional[str] = None,
        pause_duration: float = 0.6
    ) -> str:
        """Generate audio with natural pauses between sentences.
        
        Args:
            text: Text to convert to speech
            output_filename: Optional output filename
            pause_duration: Duration of pause in seconds
            
        Returns:
            Path to generated audio file
        """
        # Split text into sentences
        import re
        sentences = re.split(r'[.!?]\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        audio_segments = []
        
        for i, sentence in enumerate(sentences):
            try:
                # Generate audio for sentence (will auto-fallback if needed)
                sentence_audio = self.generate_audio(
                    sentence,
                    output_filename=f"temp_sentence_{i}.mp3"
                )
                
                # Load audio segment
                segment = AudioSegment.from_mp3(sentence_audio)
                audio_segments.append(segment)
                
                # Add pause (except after last sentence)
                if i < len(sentences) - 1:
                    pause_ms = int(pause_duration * 1000)
                    pause = AudioSegment.silent(duration=pause_ms)
                    audio_segments.append(pause)
                
                # Clean up temp file
                if os.path.exists(sentence_audio):
                    os.remove(sentence_audio)
            except Exception as e:
                logger.error(f"Error generating audio for sentence {i}: {e}")
                # Continue with other sentences
                continue
        
        # Combine all segments
        if audio_segments:
            final_audio = sum(audio_segments)
        else:
            final_audio = AudioSegment.silent(duration=1000)
        
        # Save final audio
        if output_filename is None:
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()
            output_filename = f"tts_enhanced_{text_hash}.mp3"
        
        output_path = os.path.join(self.output_dir, output_filename)
        final_audio.export(output_path, format="mp3", bitrate="192k")
        
        return output_path
    
    def get_audio_duration(self, audio_path: str) -> float:
        """Get duration of audio file in seconds."""
        audio = AudioSegment.from_mp3(audio_path)
        return len(audio) / 1000.0
