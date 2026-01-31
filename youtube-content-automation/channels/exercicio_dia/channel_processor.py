"""Processor for Exercício do Dia channel."""

import os
import random
from typing import Dict
from datetime import datetime

from core.video_generator import VideoGenerator
from core.template_engine import TemplateEngine
from core.text_to_speech_enhanced import EnhancedTextToSpeech
from core.image_processor import ImageProcessor

EXERCICIOS = [
    ("Agachamento", "Fortalece pernas e glúteos. 3 séries de 15 repetições."),
    ("Prancha", "Core forte em 30 segundos. Mantenha a postura reta."),
    ("Polichinelos", "Cardio rápido. 1 minuto de aquecimento."),
    ("Flexão", "Peito e braços. Adapte na altura se necessário."),
    ("Alongamento", "Flexibilidade e recuperação. Respire e relaxe."),
]


class ExercicioDiaProcessor:
    """Process and generate content for Exercício do Dia channel."""

    def __init__(self, output_dir: str = "outputs"):
        self.video_generator = VideoGenerator(output_dir)
        self.template_engine = TemplateEngine()
        self.tts = EnhancedTextToSpeech(output_dir)
        self.image_processor = ImageProcessor(output_dir)

    def process_exercicio(self, generate_videos: bool = True) -> Dict:
        """Process an exercise and generate videos."""
        nome, desc = random.choice(EXERCICIOS)
        short_script = f"Exercício do dia: {nome}. {desc}"
        long_script = f"{nome}\n\n{desc}\n\nCuide do seu corpo. Movimento é saúde."
        title = f"{nome} | Exercício do Dia"
        description = f"💪 {nome}\n\n{desc}\n\n#fitness #exercício #treino #saúde"
        tags = ["fitness", "exercício", nome.lower(), "treino", "bem estar"]
        result = {"title": title, "description": description, "tags": tags}
        if generate_videos:
            short_audio = self.tts.generate_audio(short_script)
            long_audio = self.tts.generate_audio(long_script)
            short_tpl = self.template_engine.get_shorts_template("exercicio_dia")
            long_tpl = self.template_engine.get_long_form_template("exercicio_dia")
            short_tpl = self.template_engine.apply_text_to_template(short_tpl, short_script, "center")
            long_tpl = self.template_engine.apply_text_to_template(long_tpl, long_script, "center")
            bg = self.image_processor.create_gradient_background(
                (1920, 1080), (40, 100, 80), (80, 140, 120),
                output_path=os.path.join(self.video_generator.output_dir, "exercicio_bg.jpg")
            )
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            result["short_video_path"] = self.video_generator.create_shorts_video(
                short_script, [bg], short_audio, short_tpl, f"exercicio_short_{ts}.mp4"
            )
            result["video_path"] = self.video_generator.create_long_form_video(
                long_script, [bg], long_audio, long_tpl, f"exercicio_long_{ts}.mp4"
            )
        return result
