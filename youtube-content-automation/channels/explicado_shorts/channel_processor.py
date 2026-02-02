"""Main processor for Explicado em Shorts channel."""

import os
import sys
from typing import Dict
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from data_sources.content_generator_enhanced import EnhancedContentGenerator
from core.video_generator import VideoGenerator
from core.template_engine import TemplateEngine
from core.text_to_speech_enhanced import EnhancedTextToSpeech
from core.image_processor import ImageProcessor


class ExplicadoShortsProcessor:
    """Process and generate content for Explicado em Shorts channel."""
    
    def __init__(self, output_dir: str = "outputs"):
        """Initialize processor.
        
        Args:
            output_dir: Output directory
        """
        self.content_generator = EnhancedContentGenerator()
        self.video_generator = VideoGenerator(output_dir)
        self.template_engine = TemplateEngine()
        # Use enhanced TTS with high-quality Brazilian Portuguese voice
        self.tts = EnhancedTextToSpeech(output_dir, voice="river")
        self.image_processor = ImageProcessor(output_dir)
    
    def process_topic(
        self,
        topic: str = None,
        category: str = None,
        generate_videos: bool = True
    ) -> Dict:
        """Process a topic and generate educational videos.
        
        Args:
            topic: Specific topic (optional, random if not provided)
            category: Topic category (optional)
            generate_videos: Whether to generate video files
            
        Returns:
            Dictionary with video information
        """
        # Get topic
        if not topic:
            topic = self.content_generator.get_random_topic()
        
        # Generate high-quality scripts
        short_script = self.content_generator.generate_script(topic, 'short')
        long_script = self.content_generator.generate_script(topic, 'long')
        
        # Enhance description with more details
        enhanced_description = f"📚 {topic}\n\n"
        enhanced_description += f"{long_script}\n\n"
        enhanced_description += "🔔 Se inscreva no canal para mais conteúdo educativo!\n"
        enhanced_description += "👍 Deixe seu like se este vídeo foi útil!\n"
        enhanced_description += "💬 Comente qual tema você gostaria de ver explicado!\n\n"
        enhanced_description += "#educação #explicação #shorts #aprendizado"
        
        title = f"{topic} | Explicado em Shorts"
        
        description = enhanced_description
        
        tags = [
            'educação', 'explicação', 'shorts', 'aprendizado',
            topic.lower(), 'conhecimento', 'curiosidades'
        ]
        
        result = {
            'topic': topic,
            'title': title,
            'description': description,
            'tags': tags
        }
        
        if generate_videos:
            # Generate high-quality TTS with natural pauses
            short_audio = self.tts.generate_audio(short_script, rate="+5%", pitch="+0Hz")
            long_audio = self.tts.generate_audio_with_pauses(long_script, pause_duration=0.7)
            
            # Get templates
            short_template = self.template_engine.get_shorts_template('explicado_shorts')
            short_template = self.template_engine.apply_text_to_template(
                short_template, short_script, 'center'
            )
            
            long_template = self.template_engine.get_long_form_template('explicado_shorts')
            long_template = self.template_engine.apply_text_to_template(
                long_template, long_script, 'center'
            )
            
            # Background profissional: Unsplash (se API key) ou gradiente
            images = []
            kw = (topic or "education").replace("?", "").split()[0] if topic else "education"
            slug = (topic or "topic").replace(" ", "_").replace("?", "")[:25]
            bg_image = self.image_processor.create_professional_background(
                (1920, 1080),
                keyword=kw,
                palette="blue_pro",
                output_path=os.path.join(self.video_generator.output_dir, f"explicado_{slug}_bg.jpg")
            )
            images.append(bg_image)
            
            # Generate videos
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            topic_slug = topic.replace(' ', '_').replace('?', '').lower()
            
            short_video_filename = f"explicado_short_{topic_slug}_{timestamp}.mp4"
            short_video_path = self.video_generator.create_shorts_video(
                script=short_script,
                images=images,
                audio_path=short_audio,
                template_config=short_template,
                output_filename=short_video_filename
            )
            
            long_video_filename = f"explicado_long_{topic_slug}_{timestamp}.mp4"
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
