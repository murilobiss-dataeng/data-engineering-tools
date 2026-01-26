"""Video generation using MoviePy."""

import os
from typing import List, Dict, Optional, Tuple
from moviepy.editor import (
    VideoFileClip, ImageClip, CompositeVideoClip,
    ColorClip, concatenate_videoclips, AudioFileClip
)
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class VideoGenerator:
    """Generate videos with templates, text overlays, and images."""
    
    # Standard YouTube dimensions
    SHORTS_SIZE = (1080, 1920)  # 9:16 vertical
    LONG_FORM_SIZE = (1920, 1080)  # 16:9 horizontal
    
    def __init__(self, output_dir: str = "outputs"):
        """Initialize video generator.
        
        Args:
            output_dir: Directory to save generated videos
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def create_shorts_video(
        self,
        script: str,
        images: List[str],
        audio_path: str,
        template_config: Dict,
        output_filename: str
    ) -> str:
        """Create a shorts video (vertical 9:16).
        
        Args:
            script: Text script for the video
            images: List of image paths to use
            audio_path: Path to audio file (TTS)
            template_config: Template configuration dict
            output_filename: Output filename
            
        Returns:
            Path to generated video
        """
        return self._create_video(
            script=script,
            images=images,
            audio_path=audio_path,
            template_config=template_config,
            output_filename=output_filename,
            is_shorts=True
        )
    
    def create_long_form_video(
        self,
        script: str,
        images: List[str],
        audio_path: str,
        template_config: Dict,
        output_filename: str
    ) -> str:
        """Create a long-form video (horizontal 16:9).
        
        Args:
            script: Text script for the video
            images: List of image paths to use
            audio_path: Path to audio file (TTS)
            template_config: Template configuration dict
            output_filename: Output filename
            
        Returns:
            Path to generated video
        """
        return self._create_video(
            script=script,
            images=images,
            audio_path=audio_path,
            template_config=template_config,
            output_filename=output_filename,
            is_shorts=False
        )
    
    def _create_video(
        self,
        script: str,
        images: List[str],
        audio_path: str,
        template_config: Dict,
        output_filename: str,
        is_shorts: bool
    ) -> str:
        """Internal method to create video."""
        size = self.SHORTS_SIZE if is_shorts else self.LONG_FORM_SIZE
        
        # Load audio to determine duration
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        # Calculate image display duration
        if images:
            image_duration = duration / len(images)
        else:
            image_duration = duration
        
        # Create video clips from images
        video_clips = []
        for i, image_path in enumerate(images):
            if os.path.exists(image_path):
                img_clip = ImageClip(image_path, duration=min(image_duration, duration - sum([c.duration for c in video_clips])))
                img_clip = img_clip.resize(size)
                video_clips.append(img_clip)
        
        # If no images, create a solid color background
        if not video_clips:
            bg_clip = ColorClip(size=size, color=template_config.get('bg_color', (0, 0, 0)), duration=duration)
            video_clips.append(bg_clip)
        else:
            # Concatenate image clips
            if len(video_clips) > 1:
                main_clip = concatenate_videoclips(video_clips, method="compose")
            else:
                main_clip = video_clips[0]
            
            # Adjust duration to match audio
            if main_clip.duration < duration:
                main_clip = main_clip.loop(duration=duration)
            elif main_clip.duration > duration:
                main_clip = main_clip.subclip(0, duration)
        
        # Add text overlays
        text_clips = self._create_text_overlays(script, template_config, duration, size)
        
        # Composite all clips
        final_clip = CompositeVideoClip([main_clip] + text_clips)
        final_clip = final_clip.set_audio(audio_clip)
        final_clip = final_clip.set_duration(duration)
        
        # Export video with high quality settings
        output_path = os.path.join(self.output_dir, output_filename)
        final_clip.write_videofile(
            output_path,
            fps=30,  # Higher FPS for better quality
            codec='libx264',
            audio_codec='aac',
            bitrate='8000k',  # High bitrate for quality
            audio_bitrate='192k',  # High audio quality
            preset='slow',  # Better quality encoding
            threads=4,
            logger=None  # Reduce verbose output
        )
        
        # Cleanup
        audio_clip.close()
        final_clip.close()
        
        return output_path
    
    def _create_text_overlays(
        self,
        script: str,
        template_config: Dict,
        duration: float,
        size: Tuple[int, int]
    ) -> List[ImageClip]:
        """Create text overlay clips using PIL (no ImageMagick required)."""
        text_clips = []
        text_elements = template_config.get('text_elements', [])
        
        for i, element in enumerate(text_elements):
            text = element.get('text', '')
            if not text:
                continue
                
            position = element.get('position', 'center')
            fontsize = element.get('fontsize', 50)
            color = element.get('color', 'white')
            font_name = element.get('font', 'Arial-Bold')
            bg_color = element.get('bg_color')
            stroke_color = element.get('stroke_color', 'black')
            stroke_width = element.get('stroke_width', 2)
            
            # Convert color string to RGB tuple
            if isinstance(color, str):
                color_map = {
                    'white': (255, 255, 255),
                    'black': (0, 0, 0),
                    'red': (255, 0, 0),
                    'green': (0, 255, 0),
                    'blue': (0, 0, 255),
                    'yellow': (255, 255, 0)
                }
                text_color = color_map.get(color.lower(), (255, 255, 255))
            else:
                text_color = color
            
            if isinstance(stroke_color, str):
                stroke_rgb = color_map.get(stroke_color.lower(), (0, 0, 0))
            else:
                stroke_rgb = stroke_color if stroke_color else (0, 0, 0)
            
            # Create text image using PIL
            max_width = int(size[0] * 0.9)
            
            # Try to load font
            try:
                # Try common font paths
                font_paths = [
                    f'/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                    f'/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
                    '/System/Library/Fonts/Helvetica.ttc',  # macOS
                ]
                font_obj = None
                for path in font_paths:
                    if os.path.exists(path):
                        font_obj = ImageFont.truetype(path, fontsize)
                        break
                
                if font_obj is None:
                    font_obj = ImageFont.load_default()
            except:
                font_obj = ImageFont.load_default()
            
            # Calculate text size with word wrapping
            words = text.split(' ')
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox(
                    (0, 0), test_line, font=font_obj
                )
                text_width = bbox[2] - bbox[0]
                
                if text_width <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            if not lines:
                lines = [text]
            
            # Calculate image size
            line_heights = []
            for line in lines:
                bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox(
                    (0, 0), line, font=font_obj
                )
                line_heights.append(bbox[3] - bbox[1])
            
            line_height = max(line_heights) if line_heights else fontsize
            total_height = len(lines) * line_height + (len(lines) - 1) * int(line_height * 0.2)
            total_height += 40  # Padding
            
            # Create image
            img_width = max_width + 40
            img_height = total_height
            
            if bg_color:
                if isinstance(bg_color, (list, tuple)) and len(bg_color) >= 3:
                    bg_rgb = tuple(bg_color[:3])
                else:
                    bg_rgb = (0, 0, 0)
                img = Image.new('RGB', (img_width, img_height), bg_rgb)
            else:
                img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
            
            draw = ImageDraw.Draw(img)
            
            # Draw text lines
            y_offset = 20
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font_obj)
                text_width = bbox[2] - bbox[0]
                x = (img_width - text_width) // 2
                
                # Draw stroke (outline)
                if stroke_width > 0:
                    for adj_x in range(-stroke_width, stroke_width + 1):
                        for adj_y in range(-stroke_width, stroke_width + 1):
                            draw.text(
                                (x + adj_x, y_offset + adj_y),
                                line,
                                font=font_obj,
                                fill=stroke_rgb
                            )
                
                # Draw text
                draw.text((x, y_offset), line, font=font_obj, fill=text_color)
                y_offset += line_height + int(line_height * 0.2)
            
            # Convert PIL image to numpy array
            img_array = np.array(img)
            
            # Create ImageClip from numpy array
            txt_clip = ImageClip(img_array, duration=duration)
            
            # Set position
            if isinstance(position, str):
                if position == 'top':
                    pos = ('center', 50)
                elif position == 'bottom':
                    pos = ('center', size[1] - img_height - 50)
                else:
                    pos = ('center', 'center')
            else:
                pos = position
            
            txt_clip = txt_clip.set_position(pos).set_duration(duration)
            text_clips.append(txt_clip)
        
        return text_clips
    
    def create_thumbnail(
        self,
        title: str,
        image_path: Optional[str] = None,
        template_config: Dict = None,
        output_path: str = None
    ) -> str:
        """Create a thumbnail image for the video.
        
        Args:
            title: Video title
            image_path: Optional background image
            template_config: Template configuration
            output_path: Output path for thumbnail
            
        Returns:
            Path to generated thumbnail
        """
        if template_config is None:
            template_config = {}
        
        size = template_config.get('thumbnail_size', self.LONG_FORM_SIZE)
        
        # Create base image
        if image_path and os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize(size, Image.Resampling.LANCZOS)
        else:
            bg_color = template_config.get('bg_color', (0, 0, 0))
            img = Image.new('RGB', size, bg_color)
        
        # Add text overlay
        draw = ImageDraw.Draw(img)
        
        # Try to load font
        try:
            font_size = template_config.get('title_fontsize', 80)
            font_path = template_config.get('font_path')
            if font_path and os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Calculate text position
        text_color = template_config.get('title_color', (255, 255, 255))
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size[0] - text_width) // 2
        y = size[1] // 2 - text_height // 2
        
        # Draw text with outline
        outline_width = template_config.get('outline_width', 3)
        outline_color = template_config.get('outline_color', (0, 0, 0))
        
        for adj in range(-outline_width, outline_width + 1):
            for adj2 in range(-outline_width, outline_width + 1):
                draw.text((x + adj, y + adj2), title, font=font, fill=outline_color)
        
        draw.text((x, y), title, font=font, fill=text_color)
        
        # Save thumbnail
        if output_path is None:
            output_path = os.path.join(self.output_dir, 'thumbnail.jpg')
        
        img.save(output_path, 'JPEG', quality=95)
        return output_path
