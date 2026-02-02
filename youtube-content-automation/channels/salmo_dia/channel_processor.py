"""
Processor for Salmo do Dia channel – Salmos e passagens da Bíblia em um só canal.

Conteúdo unificado:
- Salmos (livro de Salmos, 150 no total – Antigo Testamento)
- Passagens da Bíblia (Evangelhos, Provérbios, Isaías, etc.)

Features:
- Texto sincronizado com áudio
- Sistema visual premium
- Publicação multi-destino (YouTube, Twitter, Kwai, IG, etc.)
"""

import os
import random
from typing import Dict, Optional, List, Tuple
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from core.text_to_speech_enhanced import EnhancedTextToSpeech
from core.synced_video_generator import SyncedVideoGenerator
from data.salmos_completos import SALMOS_COMPLETOS, MOOD_TO_PALETTE as SALMO_MOOD
from data.passagens_biblia import PASSAGENS_BIBLIA, MOOD_TO_PALETTE as PASSAGEM_MOOD

# Lista unificada: (tipo, nome, texto, mood)
def _build_content_items() -> List[Tuple[str, str, str, str]]:
    items = []
    for (nome, texto, mood) in SALMOS_COMPLETOS:
        items.append(("salmo", nome, texto, mood))
    for (ref, texto, mood) in PASSAGENS_BIBLIA:
        items.append(("passagem", ref, texto, mood))
    return items

CONTENT_ITEMS = _build_content_items()

def _palette(mood: str) -> str:
    return PASSAGEM_MOOD.get(mood) or SALMO_MOOD.get(mood, "heavenly")


class SalmoDiaProcessor:
    """
    Processador do canal Salmo do Dia: salmos e passagens da Bíblia em um só canal.
    Índices 0..N-1 = salmos; N..N+M-1 = passagens.
    """

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.tts = EnhancedTextToSpeech(output_dir, voice="river")
        self.video_generator = SyncedVideoGenerator(output_dir)

    def _get_item(self, index: Optional[int]) -> Tuple[str, str, str, str]:
        if index is not None:
            if index < 0 or index >= len(CONTENT_ITEMS):
                raise ValueError(f"Índice inválido. Use 0-{len(CONTENT_ITEMS)-1}")
            return CONTENT_ITEMS[index]
        return random.choice(CONTENT_ITEMS)

    def process_salmo(
        self,
        generate_videos: bool = True,
        salmo_index: Optional[int] = None,
    ) -> Dict:
        """
        Processa um item (salmo ou passagem) e gera vídeos sincronizados.
        salmo_index: índice na lista unificada (0 = primeiro salmo, depois passagens). None = aleatório.
        """
        tipo, nome, texto, mood = self._get_item(salmo_index)
        palette = _palette(mood)
        title = f"{nome} | Salmo do Dia"
        description = self._create_description(nome, texto)
        tags = self._create_tags(nome, mood)

        result = {
            "title": title,
            "description": description,
            "tags": tags,
            "psalm_name": nome,
            "content_type": tipo,
            "psalm_text": texto,
            "mood": mood,
            "palette": palette,
        }

        if not generate_videos:
            return result

        result = self._generate_synced_videos(
            name=nome,
            text=texto,
            palette=palette,
            result=result,
            filename_prefix=tipo,
        )
        return result

    def _generate_synced_videos(
        self,
        name: str,
        text: str,
        palette: str,
        result: Dict,
        filename_prefix: str = "salmo",
    ) -> Dict:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"\n{'='*60}", flush=True)
        print(f"  GERANDO {name} (SHORT)", flush=True)
        print(f"  Paleta: {palette}", flush=True)
        print(f"{'='*60}\n", flush=True)

        full_script = f"{name}.\n\n{text}"
        print("  [1/2] Gerando áudio com ElevenLabs...", flush=True)
        audio_path = self.tts.generate_audio(full_script)
        print("  [2/2] Gerando Short sincronizado...", flush=True)
        short_path = self.video_generator.create_synced_video(
            title=name,
            full_text=text,
            audio_path=audio_path,
            output_filename=f"{filename_prefix}_{timestamp}.mp4",
            is_shorts=True,
            palette=palette,
            max_lines_per_page=4,
        )
        result["short_video_path"] = short_path
        result["video_path"] = short_path
        result["audio_path"] = audio_path
        print(f"\n  ✅ SHORT GERADO: {short_path}\n", flush=True)
        return result

    def _create_description(self, name: str, text: str) -> str:
        return f"""📖 {name}

{text}

---
🙏 Inscreva-se e ative o sininho. Salmos e passagens da Bíblia.

#salmo #bíblia #palavradeDeus #reflexão #fé #espiritualidade #oração #cristão"""

    def _create_tags(self, name: str, mood: str) -> List[str]:
        base = [
            "salmo", "bíblia", "palavra de deus", "reflexão", "fé",
            "espiritualidade", "oração", "cristão", "shorts", "jesus",
            name.lower().replace(" ", ""),
        ]
        mood_tags = {
            "peace": ["paz", "descanso"], "protection": ["proteção", "refúgio"],
            "hope": ["esperança", "luz"], "praise": ["louvor", "adoração"],
            "trust": ["confiança", "fé"], "repentance": ["perdão", "misericórdia"],
            "love": ["amor", "graça"], "wisdom": ["sabedoria"],
        }
        if mood in mood_tags:
            base.extend(mood_tags[mood])
        return base

    def publish_to_destinations(
        self,
        video_path: str,
        psalm_name: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        destinations: Optional[List[str]] = None,
    ) -> Dict:
        from core.publishers import publish_to_destinations, parse_destinations
        dest_list = destinations if destinations is not None else parse_destinations(None)
        for d in dest_list:
            print(f"  📤 Publicando em {d}...", flush=True)
        results = publish_to_destinations(
            video_path=video_path,
            title=f"{psalm_name} | Salmo do Dia",
            description=description or "",
            content_name=psalm_name,
            channel_label="Salmo do Dia",
            tags=tags,
            destinations=dest_list,
        )
        for dest_id, r in results.items():
            if isinstance(r, dict) and r.get("url"):
                print(f"  ✅ {dest_id}: {r.get('url')}", flush=True)
            elif isinstance(r, dict) and r.get("error"):
                print(f"  ⚠️ {dest_id}: {r.get('error')}", flush=True)
        return results

    def process_and_publish(
        self,
        salmo_index: Optional[int] = None,
        publish_destinations: Optional[List[str]] = None,
    ) -> Dict:
        result = self.process_salmo(generate_videos=True, salmo_index=salmo_index)
        if result.get("short_video_path"):
            dest_list = publish_destinations if publish_destinations is not None else None
            if dest_list is not None and len(dest_list) == 0:
                dest_list = None
            pub = self.publish_to_destinations(
                video_path=result["short_video_path"],
                psalm_name=result.get("psalm_name", "Salmo do Dia"),
                description=result.get("description", ""),
                tags=result.get("tags"),
                destinations=dest_list,
            )
            result["publish"] = pub
            result["twitter"] = pub.get("twitter")
        return result

    @staticmethod
    def list_available_salmos() -> None:
        """Lista todo o conteúdo do canal: salmos e passagens."""
        print(f"\n{'='*60}")
        print("  SALMO DO DIA – Salmos e passagens da Bíblia")
        print(f"{'='*60}\n")
        n_salmos = len(SALMOS_COMPLETOS)
        n_passagens = len(PASSAGENS_BIBLIA)
        for i, (tipo, nome, texto, mood) in enumerate(CONTENT_ITEMS):
            linhas = len([l for l in texto.strip().split("\n") if l.strip()])
            pal = _palette(mood)
            print(f"  [{i:3d}] {tipo:<8} | {nome:<18} | {linhas:2d} linhas | {mood:<10} | {pal}")
        print(f"\n{'='*60}")
        print(f"  Salmos: {n_salmos} | Passagens: {n_passagens} | Total: {len(CONTENT_ITEMS)}")
        print(f"{'='*60}\n")

    @staticmethod
    def get_salmo_info(index: int) -> Optional[Dict]:
        if index < 0 or index >= len(CONTENT_ITEMS):
            return None
        tipo, nome, texto, mood = CONTENT_ITEMS[index]
        linhas = [l.strip() for l in texto.strip().split("\n") if l.strip()]
        return {
            "index": index,
            "nome": nome,
            "content_type": tipo,
            "texto": texto,
            "mood": mood,
            "palette": _palette(mood),
            "num_versos": len(linhas),
            "versos": linhas,
        }


def gerar_salmo_do_dia(
    salmo_index: Optional[int] = None,
    publish_destinations: Optional[List[str]] = None,
    output_dir: str = "outputs",
) -> Dict:
    processor = SalmoDiaProcessor(output_dir=output_dir)
    if publish_destinations is not None:
        return processor.process_and_publish(salmo_index=salmo_index, publish_destinations=publish_destinations)
    return processor.process_salmo(generate_videos=True, salmo_index=salmo_index)


if __name__ == "__main__":
    SalmoDiaProcessor.list_available_salmos()
