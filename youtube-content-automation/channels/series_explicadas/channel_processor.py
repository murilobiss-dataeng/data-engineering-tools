"""Main processor for Series Explicadas channel."""

import os
import sys
from typing import Dict
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from .series_analyzer import SeriesAnalyzer
from core.video_generator import VideoGenerator
from core.template_engine import TemplateEngine
from core.text_to_speech import TextToSpeech
from core.image_processor import ImageProcessor


class SeriesExplicadasProcessor:
    """Process and generate content for Series Explicadas channel."""
    
    def __init__(self, output_dir: str = "outputs"):
        """Initialize processor.
        
        Args:
            output_dir: Output directory
        """
        self.series_analyzer = SeriesAnalyzer()
        self.video_generator = VideoGenerator(output_dir)
        self.template_engine = TemplateEngine()
        # Use Brazilian Portuguese TLD for better voice quality
        self.tts = TextToSpeech(output_dir, language='pt', slow=False, tld='com.br')
        self.image_processor = ImageProcessor(output_dir)
    
    def process_series(
        self,
        series_id: int = None,
        generate_videos: bool = True
    ) -> Dict:
        """Process a TV series and generate explanation videos.
        
        Args:
            series_id: TMDB series ID (random if not provided)
            generate_videos: Whether to generate video files
            
        Returns:
            Dictionary with video information
        """
        # Get series
        if not series_id:
            random_series = self.series_analyzer.get_random_series()
            series_id = random_series.get('id')
        
        if not series_id:
            return {}
        
        # Analyze series
        analysis = self.series_analyzer.analyze_series(series_id)
        
        if not analysis:
            return {}
        
        name = analysis.get('name', '')
        
        # Generate scripts
        long_script = self.series_analyzer.generate_series_script(analysis, 'long')
        short_script = self.series_analyzer.generate_series_script(analysis, 'short')
        
        title = f"{name} Explicada | Sem Spoilers | Series Explicadas"
        
        description = f"Explicação completa sobre a série: {name}\n\n"
        description += f"{analysis.get('overview', '')}\n\n"
        description += "⚠️ Este vídeo não contém spoilers!\n"
        description += "Apenas informações gerais sobre a série.\n\n"
        description += "Não esqueça de se inscrever e deixar seu like!"
        
        tags = [
            'séries', 'tv', 'explicação', name.lower(),
            'sem spoilers', 'resumo', 'análise'
        ]
        
        result = {
            'series_id': series_id,
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
            long_template = self.template_engine.get_long_form_template('series_explicadas')
            long_template = self.template_engine.apply_text_to_template(
                long_template, long_script, 'center'
            )
            
            short_template = self.template_engine.get_shorts_template('series_explicadas')
            short_template = self.template_engine.apply_text_to_template(
                short_template, short_script, 'center'
            )
            
            # Download poster image if available
            images = []
            poster_url = analysis.get('poster_url', '')
            
            if poster_url:
                try:
                    poster_path = self.image_processor.download_image(
                        poster_url,
                        output_path=os.path.join(
                            self.video_generator.output_dir,
                            f"series_{series_id}_poster.jpg"
                        )
                    )
                    # Resize for video
                    poster_resized = self.image_processor.resize_image(
                        poster_path,
                        (1920, 1080),
                        maintain_aspect=True
                    )
                    images.append(poster_resized)
                except Exception as e:
                    print(f"Error downloading poster: {e}")
            
            # Fallback to gradient if no poster
            if not images:
                bg_image = self.image_processor.create_gradient_background(
                    (1920, 1080),
                    (50, 0, 100),  # Purple gradient
                    (100, 0, 150),
                    output_path=os.path.join(
                        self.video_generator.output_dir,
                        f"series_{series_id}_bg.jpg"
                    )
                )
                images.append(bg_image)
            
            # Generate videos
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name_slug = name.replace(' ', '_').lower()
            
            short_video_filename = f"series_short_{name_slug}_{timestamp}.mp4"
            short_video_path = self.video_generator.create_shorts_video(
                script=short_script,
                images=images,
                audio_path=short_audio,
                template_config=short_template,
                output_filename=short_video_filename
            )
            
            long_video_filename = f"series_long_{name_slug}_{timestamp}.mp4"
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
