"""Processor for Curiosidade do Dia channel."""

import os
import random
from typing import Dict
from datetime import datetime

from core.video_generator import VideoGenerator
from core.template_engine import TemplateEngine
from core.text_to_speech_enhanced import EnhancedTextToSpeech
from core.image_processor import ImageProcessor

CURIOSIDADES = [
    ("Abelhas", "Abelhas reconhecem rostos humanos e podem contar até 4."),
    ("Medusa", "A água-viva Turritopsis é biologicamente imortal."),
    ("Bactérias", "Existem mais bactérias no corpo que células humanas."),
    ("Oceano", "Mais de 80% do oceano permanece inexplorado."),
    ("Cérebro", "O cérebro gera cerca de 70 mil pensamentos por dia."),
]


class CuriosidadeDiaProcessor:
    """Process and generate content for Curiosidade do Dia channel."""

    def __init__(self, output_dir: str = "outputs"):
        self.video_generator = VideoGenerator(output_dir)
        self.template_engine = TemplateEngine()
        self.tts = EnhancedTextToSpeech(output_dir)
        self.image_processor = ImageProcessor(output_dir)

    def process_curiosidade(self, generate_videos: bool = True) -> Dict:
        """Process curiosity content and generate videos."""
        tema, curiosidade = random.choice(CURIOSIDADES)
        short_script = f"Curiosidade do dia: {tema}. {curiosidade}"
        long_script = f"Top 10: {tema}\n\n{curiosidade}\n\nCurioso? Deixe o like!"
        title = f"{tema} | Curiosidade do Dia"
        description = f"🔍 {tema}\n\n{curiosidade}\n\n#curiosidade #top10 #conhecimento"
        tags = ["curiosidade", "top 10", tema.lower(), "conhecimento"]
        result = {"title": title, "description": description, "tags": tags}
        if generate_videos:
            short_audio = self.tts.generate_audio(short_script)
            long_audio = self.tts.generate_audio(long_script)
            short_tpl = self.template_engine.get_shorts_template("curiosidade_dia")
            long_tpl = self.template_engine.get_long_form_template("curiosidade_dia")
            short_tpl = self.template_engine.apply_text_to_template(short_tpl, short_script, "center")
            long_tpl = self.template_engine.apply_text_to_template(long_tpl, long_script, "center")
            bg = self.image_processor.create_gradient_background(
                (1920, 1080), (60, 80, 120), (100, 120, 180),
                output_path=os.path.join(self.video_generator.output_dir, "curiosidade_bg.jpg")
            )
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            result["short_video_path"] = self.video_generator.create_shorts_video(
                short_script, [bg], short_audio, short_tpl, f"curiosidade_short_{ts}.mp4"
            )
            result["video_path"] = self.video_generator.create_long_form_video(
                long_script, [bg], long_audio, long_tpl, f"curiosidade_long_{ts}.mp4"
            )
        return result
