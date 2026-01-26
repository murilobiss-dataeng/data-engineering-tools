"""Main processor for Quanto rende? channel."""

import os
import sys
from typing import Dict
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from .investment_simulator import InvestmentSimulator
from core.video_generator import VideoGenerator
from core.template_engine import TemplateEngine
from core.text_to_speech import TextToSpeech
from core.image_processor import ImageProcessor


class QuantoRendeProcessor:
    """Process and generate content for Quanto rende? channel."""
    
    def __init__(self, output_dir: str = "outputs"):
        """Initialize processor.
        
        Args:
            output_dir: Output directory
        """
        self.simulator = InvestmentSimulator()
        self.video_generator = VideoGenerator(output_dir)
        self.template_engine = TemplateEngine()
        # Use Brazilian Portuguese TLD for better voice quality
        self.tts = TextToSpeech(output_dir, language='pt', slow=False, tld='com.br')
        self.image_processor = ImageProcessor(output_dir)
    
    def process_investment(
        self,
        investment: Dict = None,
        generate_videos: bool = True
    ) -> Dict:
        """Process an investment and generate simulation videos.
        
        Args:
            investment: Investment dictionary (random if not provided)
            generate_videos: Whether to generate video files
            
        Returns:
            Dictionary with video information
        """
        # Get investment scenario
        if not investment:
            investment = self.simulator.get_random_investment()
        
        # Simulate investment
        simulation = self.simulator.simulate_investment(investment)
        
        # Generate explanation
        explanation = self.simulator.generate_explanation(simulation)
        
        investment_type = investment.get('type', 'Investimento')
        principal = investment.get('principal', 0)
        
        title = f"Quanto rende R$ {principal:,.0f} em {investment_type}? | Cálculo Completo"
        
        description = f"Simulação completa de quanto rende R$ {principal:,.0f} investido em {investment_type}.\n\n"
        description += explanation + "\n\n"
        description += "⚠️ Esta é uma simulação baseada em taxas atuais.\n"
        description += "Valores reais podem variar.\n"
        description += "Consulte um consultor financeiro antes de investir.\n\n"
        description += "Não esqueça de se inscrever e deixar seu like!"
        
        tags = [
            'investimento', 'rendimento', 'simulação', investment_type.lower(),
            'finanças', 'dinheiro', 'cálculo', 'lucro'
        ]
        
        result = {
            'investment': investment,
            'simulation': simulation,
            'title': title,
            'description': description,
            'tags': tags
        }
        
        if generate_videos:
            # Generate scripts
            short_script = f"Quanto rende R$ {principal:,.0f} em {investment_type}?\n\n"
            short_script += f"Valor líquido: R$ {simulation.get('net_amount', 0):,.2f}\n"
            short_script += f"Lucro: R$ {simulation.get('net_profit', 0):,.2f}\n\n"
            short_script += "Veja o cálculo completo no vídeo!"
            
            long_script = f"Olá! Bem-vindo ao Quanto Rende?\n\n"
            long_script += explanation
            
            # Generate TTS
            short_audio = self.tts.generate_audio(short_script)
            long_audio = self.tts.generate_audio_with_pauses(long_script)
            
            # Get templates
            short_template = self.template_engine.get_shorts_template('quanto_rende')
            short_template = self.template_engine.apply_text_to_template(
                short_template, short_script, 'center'
            )
            
            long_template = self.template_engine.get_long_form_template('quanto_rende')
            long_template = self.template_engine.apply_text_to_template(
                long_template, long_script, 'center'
            )
            
            # Create images
            images = []
            bg_image = self.image_processor.create_gradient_background(
                (1920, 1080),
                (0, 100, 50),  # Green gradient for money
                (0, 150, 100),
                output_path=os.path.join(
                    self.video_generator.output_dir,
                    f"quanto_rende_{investment_type.replace(' ', '_')}_bg.jpg"
                )
            )
            images.append(bg_image)
            
            # Generate videos
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            investment_slug = investment_type.replace(' ', '_').lower()
            
            short_video_filename = f"quanto_rende_short_{investment_slug}_{timestamp}.mp4"
            short_video_path = self.video_generator.create_shorts_video(
                script=short_script,
                images=images,
                audio_path=short_audio,
                template_config=short_template,
                output_filename=short_video_filename
            )
            
            long_video_filename = f"quanto_rende_long_{investment_slug}_{timestamp}.mp4"
            long_video_path = self.video_generator.create_long_form_video(
                script=long_script,
                images=images,
                audio_path=long_audio,
                template_config=long_template,
                output_filename=long_video_filename
            )
            
            result['short_video_path'] = short_video_path
            result['video_path'] = long_video_path
        
        return result
