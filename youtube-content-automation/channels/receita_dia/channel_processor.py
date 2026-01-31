"""Processor for Receita do Dia channel."""

import os
import random
from typing import Dict
from datetime import datetime

from core.video_generator import VideoGenerator
from core.template_engine import TemplateEngine
from core.text_to_speech_enhanced import EnhancedTextToSpeech
from core.image_processor import ImageProcessor

RECEITAS = [
    ("Bolo de Cenoura", "Fácil, fofinho e delicioso. Ingredientes: cenoura, ovos, farinha."),
    ("Frango Grelhado", "Proteína magra e saborosa. Temperos: alho, limão, ervas."),
    ("Salada Caesar", "Clássica e nutritiva. Molho cremoso e croûtons."),
    ("Suco Detox", "Desintoxique com verde. Couve, abacaxi, gengibre."),
    ("Omelete Fit", "Café da manhã proteico. Ovos, queijo e temperos."),
]


class ReceitaDiaProcessor:
    """Process and generate content for Receita do Dia channel."""

    def __init__(self, output_dir: str = "outputs"):
        self.video_generator = VideoGenerator(output_dir)
        self.template_engine = TemplateEngine()
        self.tts = EnhancedTextToSpeech(output_dir)
        self.image_processor = ImageProcessor(output_dir)

    def process_receita(self, generate_videos: bool = True) -> Dict:
        """Process a recipe and generate videos."""
        nome, desc = random.choice(RECEITAS)
        short_script = f"Receita do dia: {nome}. {desc}"
        long_script = f"{nome}\n\n{desc}\n\nConfira o passo a passo completo no vídeo."
        title = f"{nome} | Receita do Dia"
        description = f"🍳 {nome}\n\n{desc}\n\n#receita #culinária #comida"
        tags = ["receita", "culinária", nome.lower(), "comida", "chef"]
        result = {"title": title, "description": description, "tags": tags}
        if generate_videos:
            short_audio = self.tts.generate_audio(short_script)
            long_audio = self.tts.generate_audio(long_script)
            short_tpl = self.template_engine.get_shorts_template("receita_dia")
            long_tpl = self.template_engine.get_long_form_template("receita_dia")
            short_tpl = self.template_engine.apply_text_to_template(short_tpl, short_script, "center")
            long_tpl = self.template_engine.apply_text_to_template(long_tpl, long_script, "center")
            bg = self.image_processor.create_gradient_background(
                (1920, 1080), (180, 80, 60), (220, 120, 100),
                output_path=os.path.join(self.video_generator.output_dir, "receita_bg.jpg")
            )
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            result["short_video_path"] = self.video_generator.create_shorts_video(
                short_script, [bg], short_audio, short_tpl, f"receita_short_{ts}.mp4"
            )
            result["video_path"] = self.video_generator.create_long_form_video(
                long_script, [bg], long_audio, long_tpl, f"receita_long_{ts}.mp4"
            )
        return result
