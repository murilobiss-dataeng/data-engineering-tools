"""Main processor for Bets do Dia channel."""

import os
import sys
from typing import Dict
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from data_sources.football_api import FootballAPI
from core.video_generator import VideoGenerator
from core.template_engine import TemplateEngine
from core.text_to_speech import TextToSpeech
from core.image_processor import ImageProcessor
from .bet_analyzer import BetAnalyzer
from .risk_calculator import RiskCalculator


class BetsDiaProcessor:
    """Process and generate content for Bets do Dia channel."""
    
    def __init__(self, output_dir: str = "outputs"):
        """Initialize processor.
        
        Args:
            output_dir: Output directory
        """
        self.football_api = FootballAPI()
        self.bet_analyzer = BetAnalyzer(self.football_api)
        self.risk_calculator = RiskCalculator()
        self.video_generator = VideoGenerator(output_dir)
        self.template_engine = TemplateEngine()
        # Use Brazilian Portuguese TLD for better voice quality
        self.tts = TextToSpeech(output_dir, language='pt', slow=False, tld='com.br')
        self.image_processor = ImageProcessor(output_dir)
    
    def process_match_bet(self, fixture_id: int, generate_videos: bool = True) -> Dict:
        """Process a match and generate betting analysis videos.
        
        Args:
            fixture_id: Fixture ID
            generate_videos: Whether to generate video files
            
        Returns:
            Dictionary with video information
        """
        # Analyze match for betting
        analysis = self.bet_analyzer.analyze_match_for_betting(fixture_id)
        
        if not analysis:
            return {}
        
        home_team = analysis.get('home_team', '')
        away_team = analysis.get('away_team', '')
        
        # Generate scripts
        long_script = self.bet_analyzer.generate_bet_script(analysis, 'long')
        short_script = self.bet_analyzer.generate_bet_script(analysis, 'short')
        
        title = f"Análise de Apostas: {home_team} vs {away_team} | Bets do Dia"
        
        description = f"⚠️ CONTEÚDO PARA MAIORES DE 18 ANOS ⚠️\n\n"
        description += f"Análise completa de apostas para o jogo entre {home_team} e {away_team}.\n\n"
        description += "AVISOS IMPORTANTES:\n"
        description += "- Apostas envolvem risco de perda financeira\n"
        description += "- Nunca aposte mais do que pode perder\n"
        description += "- Jogue com responsabilidade\n"
        description += "- Este conteúdo é apenas para fins informativos\n\n"
        description += "Não esqueça de se inscrever e deixar seu like!"
        
        tags = [
            'apostas', 'bets', 'futebol', home_team, away_team,
            'análise', 'probabilidades', '18+', 'jogo responsável'
        ]
        
        result = {
            'fixture_id': fixture_id,
            'title': title,
            'description': description,
            'tags': tags,
            'analysis': analysis
        }
        
        if generate_videos:
            # Generate TTS
            long_audio = self.tts.generate_audio_with_pauses(long_script)
            short_audio = self.tts.generate_audio(short_script)
            
            # Get templates
            long_template = self.template_engine.get_long_form_template('bets_dia')
            long_template = self.template_engine.apply_text_to_template(
                long_template, long_script, 'center'
            )
            
            short_template = self.template_engine.get_shorts_template('bets_dia')
            short_template = self.template_engine.apply_text_to_template(
                short_template, short_script, 'center'
            )
            
            # Create images
            images = []
            bg_image = self.image_processor.create_gradient_background(
                (1920, 1080),
                (100, 0, 0),  # Red gradient for warning
                (150, 0, 0),
                output_path=os.path.join(
                    self.video_generator.output_dir,
                    f"bet_{fixture_id}_bg.jpg"
                )
            )
            images.append(bg_image)
            
            # Generate videos
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            long_video_filename = f"bets_dia_{fixture_id}_{timestamp}.mp4"
            long_video_path = self.video_generator.create_long_form_video(
                script=long_script,
                images=images,
                audio_path=long_audio,
                template_config=long_template,
                output_filename=long_video_filename
            )
            
            short_video_filename = f"bets_dia_short_{fixture_id}_{timestamp}.mp4"
            short_video_path = self.video_generator.create_shorts_video(
                script=short_script,
                images=images,
                audio_path=short_audio,
                template_config=short_template,
                output_filename=short_video_filename
            )
            
            result['video_path'] = long_video_path
            result['short_video_path'] = short_video_path
        
        return result
