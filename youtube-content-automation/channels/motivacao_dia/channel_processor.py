"""Processor for Motivação do Dia channel."""

import os
import random
from typing import Dict
from datetime import datetime

from core.video_generator import VideoGenerator
from core.template_engine import TemplateEngine
from core.text_to_speech_enhanced import EnhancedTextToSpeech
from core.image_processor import ImageProcessor

FRASES = [
    ("Persistência", "A persistência vence o que o talento não conquista."),
    ("Comece", "O melhor momento para começar foi ontem. O segundo melhor é agora."),
    ("Falhas", "Cada falha é um passo mais perto do sucesso."),
    ("Sonhos", "Sonhe grande, comece pequeno, aja agora."),
    ("Disciplina", "A disciplina supera a motivação quando ela acaba."),
]


class MotivacaoDiaProcessor:
    """Process and generate content for Motivação do Dia channel."""

    def __init__(self, output_dir: str = "outputs"):
        self.video_generator = VideoGenerator(output_dir)
        self.template_engine = TemplateEngine()
        self.tts = EnhancedTextToSpeech(output_dir)
        self.image_processor = ImageProcessor(output_dir)

    def process_motivacao(self, generate_videos: bool = True) -> Dict:
        """Process motivation content and generate videos."""
        tema, frase = random.choice(FRASES)
        short_script = f"Motivação do dia: {tema}. {frase}"
        long_script = f"{tema}\n\n{frase}\n\nReflita e inspire-se hoje."
        title = f"{tema} | Motivação do Dia"
        description = f"🔥 {tema}\n\n{frase}\n\n#motivação #desenvolvimento #mindset"
        tags = ["motivação", "desenvolvimento pessoal", tema.lower(), "inspiração"]
        result = {"title": title, "description": description, "tags": tags}
        if generate_videos:
            short_audio = self.tts.generate_audio(short_script)
            long_audio = self.tts.generate_audio(long_script)
            short_tpl = self.template_engine.get_shorts_template("motivacao_dia")
            long_tpl = self.template_engine.get_long_form_template("motivacao_dia")
            short_tpl = self.template_engine.apply_text_to_template(short_tpl, short_script, "center")
            long_tpl = self.template_engine.apply_text_to_template(long_tpl, long_script, "center")
            bg = self.image_processor.create_gradient_background(
                (1920, 1080), (120, 60, 80), (180, 100, 140),
                output_path=os.path.join(self.video_generator.output_dir, "motivacao_bg.jpg")
            )
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            result["short_video_path"] = self.video_generator.create_shorts_video(
                short_script, [bg], short_audio, short_tpl, f"motivacao_short_{ts}.mp4"
            )
            result["video_path"] = self.video_generator.create_long_form_video(
                long_script, [bg], long_audio, long_tpl, f"motivacao_long_{ts}.mp4"
            )
        return result
