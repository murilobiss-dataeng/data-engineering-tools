"""Processor for Dica de Carreira do Dia channel."""

import os
import random
from typing import Dict
from datetime import datetime

from core.video_generator import VideoGenerator
from core.template_engine import TemplateEngine
from core.text_to_speech_enhanced import EnhancedTextToSpeech
from core.image_processor import ImageProcessor

DICAS = [
    ("LinkedIn", "Atualize seu perfil semanalmente. Perfis ativos têm 5x mais chances."),
    ("Networking", "Um café por semana com alguém da área pode mudar sua trajetória."),
    ("Feedback", "Peça feedback regularmente. Crescimento vem do que você não vê."),
    ("Aprendizado", "15 minutos por dia em um curso já faz diferença em um ano."),
    ("Entrevista", "Pesquise a empresa e prepare perguntas. Mostre interesse genuíno."),
]


class DicaCarreiraDiaProcessor:
    """Process and generate content for Dica de Carreira do Dia channel."""

    def __init__(self, output_dir: str = "outputs"):
        self.video_generator = VideoGenerator(output_dir)
        self.template_engine = TemplateEngine()
        self.tts = EnhancedTextToSpeech(output_dir)
        self.image_processor = ImageProcessor(output_dir)

    def process_dica(self, generate_videos: bool = True) -> Dict:
        """Process career tip content and generate videos."""
        tema, dica = random.choice(DICAS)
        short_script = f"Dica de carreira: {tema}. {dica}"
        long_script = f"{tema}\n\n{dica}\n\nInvista na sua carreira hoje."
        title = f"{tema} | Dica de Carreira do Dia"
        description = f"💼 {tema}\n\n{dica}\n\n#carreira #trabalho #dicas #profissional"
        tags = ["carreira", "trabalho", tema.lower(), "dicas", "emprego"]
        result = {"title": title, "description": description, "tags": tags}
        if generate_videos:
            short_audio = self.tts.generate_audio(short_script)
            long_audio = self.tts.generate_audio(long_script)
            short_tpl = self.template_engine.get_shorts_template("dica_carreira_dia")
            long_tpl = self.template_engine.get_long_form_template("dica_carreira_dia")
            short_tpl = self.template_engine.apply_text_to_template(short_tpl, short_script, "center")
            long_tpl = self.template_engine.apply_text_to_template(long_tpl, long_script, "center")
            bg = self.image_processor.create_gradient_background(
                (1920, 1080), (80, 70, 100), (120, 100, 160),
                output_path=os.path.join(self.video_generator.output_dir, "carreira_bg.jpg")
            )
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            result["short_video_path"] = self.video_generator.create_shorts_video(
                short_script, [bg], short_audio, short_tpl, f"carreira_short_{ts}.mp4"
            )
            result["video_path"] = self.video_generator.create_long_form_video(
                long_script, [bg], long_audio, long_tpl, f"carreira_long_{ts}.mp4"
            )
        return result
