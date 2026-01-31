"""Processor for Salmo do Dia channel."""

import os
from typing import Dict
from datetime import datetime

from core.video_generator import VideoGenerator
from core.template_engine import TemplateEngine
from core.text_to_speech_enhanced import EnhancedTextToSpeech
from core.image_processor import ImageProcessor


# Salmos populares para conteúdo diário
SALMOS = [
    ("Salmo 23", "O Senhor é meu pastor; nada me faltará."),
    ("Salmo 91", "Aquele que habita no esconderijo do Altíssimo..."),
    ("Salmo 27", "O Senhor é a minha luz e a minha salvação..."),
    ("Salmo 46", "Deus é o nosso refúgio e fortaleza..."),
    ("Salmo 121", "Levantarei os meus olhos para os montes..."),
]


class SalmoDiaProcessor:
    """Process and generate content for Salmo do Dia channel."""

    def __init__(self, output_dir: str = "outputs"):
        self.video_generator = VideoGenerator(output_dir)
        self.template_engine = TemplateEngine()
        self.tts = EnhancedTextToSpeech(output_dir, voice="pt-BR-FranciscaNeural")
        self.image_processor = ImageProcessor(output_dir)

    def process_salmo(self, generate_videos: bool = True) -> Dict:
        """Process a psalm and generate videos."""
        import random
        salmo_nome, versiculo = random.choice(SALMOS)
        short_script = f"{salmo_nome}. {versiculo} Reflexão do dia."
        long_script = f"{salmo_nome}\n\n{versiculo}\n\nQue esta palavra fortaleça seu dia."
        title = f"{salmo_nome} | Salmo do Dia"
        description = f"📖 {salmo_nome}\n\n{versiculo}\n\n#palavra #reflexão #fé"
        tags = ["salmo", "bíblia", "reflexão", "palavra", "fé", salmo_nome.lower()]

        result = {"title": title, "description": description, "tags": tags}
        if generate_videos:
            short_audio = self.tts.generate_audio(short_script)
            long_audio = self.tts.generate_audio(long_script)
            short_tpl = self.template_engine.get_shorts_template("salmo_dia")
            long_tpl = self.template_engine.get_long_form_template("salmo_dia")
            short_tpl = self.template_engine.apply_text_to_template(short_tpl, short_script, "center")
            long_tpl = self.template_engine.apply_text_to_template(long_tpl, long_script, "center")
            bg = self.image_processor.create_gradient_background(
                (1920, 1080), (40, 60, 100), (80, 100, 160),
                output_path=os.path.join(self.video_generator.output_dir, "salmo_bg.jpg")
            )
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            short_path = self.video_generator.create_shorts_video(
                short_script, [bg], short_audio, short_tpl, f"salmo_short_{ts}.mp4"
            )
            long_path = self.video_generator.create_long_form_video(
                long_script, [bg], long_audio, long_tpl, f"salmo_long_{ts}.mp4"
            )
            result["short_video_path"] = short_path
            result["video_path"] = long_path
        return result
