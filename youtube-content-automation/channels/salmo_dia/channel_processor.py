"""
Processor for Salmo do Dia channel – Salmos e passagens da Bíblia em um só canal.

Pipeline cinematográfico profissional:
- Backgrounds EXCLUSIVAMENTE da pasta assets/
- Narração: exclusivamente edge-tts
- Vídeo vertical 9:16 (1080x1920), Ken Burns, glow, color grading espiritual
- Tipografia elegante, fade in/out, música ambiente opcional
- Publicação multi-destino (YouTube, Twitter, Kwai, IG, etc.)
"""

import os
import random
from pathlib import Path
from typing import Dict, Optional, List, Tuple
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

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

    def __init__(self, output_dir: str = "outputs", assets_dir: Optional[str] = None):
        self.output_dir = output_dir
        self.assets_dir = assets_dir or str(Path(__file__).resolve().parents[2] / "assets")
        os.makedirs(output_dir, exist_ok=True)

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

        result = self._generate_cinematic_video(
            name=nome,
            text=texto,
            result=result,
            filename_prefix=tipo,
        )
        return result

    def _session_folder(self) -> str:
        """Pasta única por gravação: outputs/salmo_do_dia/YYYYMMDD_HHMM."""
        session_name = f"salmo_do_dia/{datetime.now().strftime('%Y%m%d_%H%M')}"
        return os.path.join(self.output_dir, session_name)

    def _generate_cinematic_video(
        self,
        name: str,
        text: str,
        result: Dict,
        filename_prefix: str = "salmo",
    ) -> Dict:
        """Gera vídeo cinematográfico: assets locais + edge-tts."""
        from core.cinematic_salmo_pipeline import run_cinematic_salmo_pipeline

        session_dir = self._session_folder()
        os.makedirs(session_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"\n{'='*60}", flush=True)
        print(f"  GERANDO {name} (SHORT CINEMATOGRÁFICO)", flush=True)
        print(f"  Pasta desta gravação: {session_dir}", flush=True)
        print(f"  Background: assets/ | Voz: edge-tts", flush=True)
        print(f"  Log: [1/6] a [6/6]. A etapa 5 (exportar MP4) costuma levar 2–5 min.", flush=True)
        print(f"{'='*60}\n", flush=True)

        try:
            out = run_cinematic_salmo_pipeline(
                title=name,
                body_text=text,
                output_dir=session_dir,
                assets_dir=self.assets_dir,
                music_path=None,
                output_filename=f"{filename_prefix}_cinematic_{timestamp}.mp4",
            )
        except RuntimeError as e:
            if "edge" in str(e).lower() or "tts" in str(e).lower():
                print("  ❌ ERRO: edge-tts falhou. Verifique: pip install edge-tts", flush=True)
            print(f"  ❌ Detalhe: {e}", flush=True)
            raise
        except FileNotFoundError as e:
            print(f"  ❌ ERRO: {e}", flush=True)
            raise
        except Exception as e:
            print(f"  ❌ ERRO inesperado: {e}", flush=True)
            raise

        short_path = out["video_path"]
        result["short_video_path"] = short_path
        result["video_path"] = short_path
        result["audio_path"] = out["audio_path"]
        result["duration_estimate_sec"] = out.get("duration_seconds", 35.0)

        # Pacote de distribuição: descrições por rede social (youtube, instagram, twitter, tiktok)
        try:
            from core.social_descriptions import save_descriptions
            desc_paths = save_descriptions(session_dir, name, text)
            result["description_files"] = desc_paths
            print(f"  📄 Descrições geradas: {', '.join(desc_paths.keys())}.txt", flush=True)
        except Exception as e:
            print(f"  ⚠️ Descrições por rede social não geradas: {e}", flush=True)
            result["description_files"] = {}

        print(f"\n  ✅ SHORT CINEMATOGRÁFICO GERADO: {short_path}\n", flush=True)
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
        result_metadata: Optional[Dict] = None,
        schedule_at: Optional[str] = None,
    ) -> Dict:
        from core.publishers import publish_to_destinations, parse_destinations
        from core.publication_options import content_hash, build_description_with_chapters
        dest_list = destinations if destinations is not None else parse_destinations(None)
        meta = result_metadata or {}
        title = f"{psalm_name} | Salmo do Dia"
        desc = description or ""
        # Tags automáticas (título + tema); capítulos na descrição; hash anti-repost
        theme = psalm_name
        duration_sec = meta.get("duration_estimate_sec")
        if duration_sec is not None and duration_sec >= 10:
            desc = build_description_with_chapters(desc, float(duration_sec))
        content_hash_val = content_hash(
            title,
            meta.get("psalm_text", meta.get("description", "")),
            meta.get("script", ""),
        )
        kwargs = {
            "theme": theme,
            "duration_estimate_sec": duration_sec,
            "description_with_chapters": desc if (duration_sec and duration_sec >= 10) else None,
            "content_hash": content_hash_val,
            "channel_namespace": "salmo_do_dia",
            "output_base_dir": self.output_dir,
        }
        if schedule_at:
            kwargs["publish_at"] = schedule_at
        for d in dest_list:
            print(f"  📤 Publicando em {d}...", flush=True)
        results = publish_to_destinations(
            video_path=video_path,
            title=title,
            description=desc,
            content_name=psalm_name,
            channel_label="Salmo do Dia",
            tags=tags,
            destinations=dest_list,
            **kwargs,
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
        schedule_at: Optional[str] = None,
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
                result_metadata=result,
                schedule_at=schedule_at,
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
