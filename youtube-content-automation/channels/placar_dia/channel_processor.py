"""Main processor for Placar do Dia channel."""

import os
import sys
from typing import List, Dict
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from data_sources.football_api import FootballAPI
from core.video_generator import VideoGenerator
from core.template_engine import TemplateEngine
from core.text_to_speech import TextToSpeech
from core.image_processor import ImageProcessor
from .match_analyzer import MatchAnalyzer
from .script_generator import ScriptGenerator


class PlacarDiaProcessor:
    """Process and generate content for Placar do Dia channel."""
    
    def __init__(
        self,
        league_id: int = None,
        output_dir: str = None
    ):
        """Initialize processor.
        
        Args:
            league_id: League ID (default: from config or env var)
            output_dir: Output directory (default: from config)
        """
        from dotenv import load_dotenv
        import yaml
        
        load_dotenv('config/api_keys.env')
        
        # Load league_id from config or env
        if league_id is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'config', 'channels.yaml'
            )
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    league_id = config.get('placar_dia', {}).get('league_id', 71)
            else:
                league_id = int(os.getenv('FOOTBALL_LEAGUE_ID', '71'))
        
        if output_dir is None:
            output_dir = os.getenv('OUTPUT_DIR', 'outputs')
        
        self.league_id = league_id
        self.football_api = FootballAPI()
        self.match_analyzer = MatchAnalyzer(self.football_api)
        self.script_generator = ScriptGenerator(self.match_analyzer)
        self.video_generator = VideoGenerator(output_dir)
        self.template_engine = TemplateEngine()
        # Use Brazilian Portuguese TLD for better voice quality
        self.tts = TextToSpeech(output_dir, language='pt', slow=False, tld='com.br')
        self.image_processor = ImageProcessor(output_dir)
    
    def process_round(self, round: str = None) -> List[Dict]:
        """Process all matches from a round.
        
        Args:
            round: Round name (optional, defaults to today's matches)
            
        Returns:
            List of generated video information
        """
        matches = self.match_analyzer.get_round_matches(self.league_id, round)
        
        results = []
        for match in matches:
            fixture_id = match.get('fixture', {}).get('id')
            if fixture_id:
                result = self.process_match(fixture_id)
                if result:
                    results.append(result)
        
        return results
    
    def process_match(self, fixture_id: int, generate_videos: bool = True) -> Dict:
        """Process a single match and generate videos.
        
        Args:
            fixture_id: Fixture ID
            generate_videos: Whether to generate video files
            
        Returns:
            Dictionary with video information
        """
        # Generate script
        script_data = self.script_generator.generate_match_script(fixture_id, 'long')
        
        if not script_data:
            return {}
        
        result = {
            'fixture_id': fixture_id,
            'title': script_data['title'],
            'description': script_data['description'],
            'tags': script_data['tags']
        }
        
        if generate_videos:
            # Generate TTS
            audio_path = self.tts.generate_audio_with_pauses(script_data['script'])
            
            # Get template
            template = self.template_engine.get_long_form_template('placar_dia')
            template = self.template_engine.apply_text_to_template(
                template, script_data['script'], 'center'
            )
            
            # Create placeholder images (in production, use actual match images)
            images = []
            match_analysis = script_data['match_analysis']
            home_team = match_analysis.get('home_team', '')
            away_team = match_analysis.get('away_team', '')
            
            # Create simple background image
            bg_image = self.image_processor.create_gradient_background(
                (1920, 1080),
                (0, 50, 100),
                (0, 100, 200),
                output_path=os.path.join(
                    self.video_generator.output_dir,
                    f"match_{fixture_id}_bg.jpg"
                )
            )
            images.append(bg_image)
            
            # Generate long-form video
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            video_filename = f"placar_dia_{fixture_id}_{timestamp}.mp4"
            video_path = self.video_generator.create_long_form_video(
                script=script_data['script'],
                images=images,
                audio_path=audio_path,
                template_config=template,
                output_filename=video_filename
            )
            
            result['video_path'] = video_path
            
            # Generate shorts version
            short_script_data = self.script_generator.generate_match_script(fixture_id, 'short')
            short_audio_path = self.tts.generate_audio(short_script_data['script'])
            short_template = self.template_engine.get_shorts_template('placar_dia')
            short_template = self.template_engine.apply_text_to_template(
                short_template, short_script_data['script'], 'center'
            )
            
            short_video_filename = f"placar_dia_short_{fixture_id}_{timestamp}.mp4"
            short_video_path = self.video_generator.create_shorts_video(
                script=short_script_data['script'],
                images=images,
                audio_path=short_audio_path,
                template_config=short_template,
                output_filename=short_video_filename
            )
            
            result['short_video_path'] = short_video_path
        
        return result
