"""Image processing utilities for video generation."""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from typing import Tuple, Optional, List
import requests
from io import BytesIO


class ImageProcessor:
    """Process and manipulate images for video generation."""
    
    def __init__(self, output_dir: str = "outputs"):
        """Initialize image processor.
        
        Args:
            output_dir: Directory to save processed images
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def resize_image(
        self,
        image_path: str,
        size: Tuple[int, int],
        output_path: Optional[str] = None,
        maintain_aspect: bool = True
    ) -> str:
        """Resize an image.
        
        Args:
            image_path: Path to input image
            size: Target size (width, height)
            output_path: Optional output path
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            Path to resized image
        """
        img = Image.open(image_path)
        
        if maintain_aspect:
            img.thumbnail(size, Image.Resampling.LANCZOS)
            # Create new image with target size and paste resized image
            new_img = Image.new('RGB', size, (0, 0, 0))
            paste_x = (size[0] - img.width) // 2
            paste_y = (size[1] - img.height) // 2
            new_img.paste(img, (paste_x, paste_y))
            img = new_img
        else:
            img = img.resize(size, Image.Resampling.LANCZOS)
        
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(self.output_dir, f"{base_name}_resized.jpg")
        
        img.save(output_path, 'JPEG', quality=95)
        return output_path
    
    def download_image(self, url: str, output_path: Optional[str] = None) -> str:
        """Download image from URL.
        
        Args:
            url: Image URL
            output_path: Optional output path
            
        Returns:
            Path to downloaded image
        """
        response = requests.get(url)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        
        if output_path is None:
            import hashlib
            url_hash = hashlib.md5(url.encode()).hexdigest()
            output_path = os.path.join(self.output_dir, f"downloaded_{url_hash}.jpg")
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img.save(output_path, 'JPEG', quality=95)
        return output_path
    
    def add_text_overlay(
        self,
        image_path: str,
        text: str,
        position: Tuple[int, int] = None,
        font_size: int = 50,
        color: Tuple[int, int, int] = (255, 255, 255),
        output_path: Optional[str] = None
    ) -> str:
        """Add text overlay to image.
        
        Args:
            image_path: Path to input image
            text: Text to add
            position: Text position (x, y), None for center
            font_size: Font size
            color: Text color (RGB)
            output_path: Optional output path
            
        Returns:
            Path to image with text overlay
        """
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Try to load font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Calculate text position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        if position is None:
            x = (img.width - text_width) // 2
            y = (img.height - text_height) // 2
        else:
            x, y = position
        
        # Draw text with outline
        outline_color = (0, 0, 0)
        for adj in range(-2, 3):
            for adj2 in range(-2, 3):
                draw.text((x + adj, y + adj2), text, font=font, fill=outline_color)
        
        draw.text((x, y), text, font=font, fill=color)
        
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(self.output_dir, f"{base_name}_text.jpg")
        
        img.save(output_path, 'JPEG', quality=95)
        return output_path
    
    def create_gradient_background(
        self,
        size: Tuple[int, int],
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int],
        output_path: Optional[str] = None,
        direction: str = 'vertical'
    ) -> str:
        """Create a professional gradient background image with subtle patterns.
        
        Args:
            size: Image size (width, height)
            color1: Start color (RGB)
            color2: End color (RGB)
            output_path: Optional output path
            direction: 'vertical' or 'horizontal'
            
        Returns:
            Path to gradient image
        """
        img = Image.new('RGB', size)
        pixels = img.load()
        
        width, height = size
        
        # Create smooth gradient
        for y in range(height):
            for x in range(width):
                if direction == 'vertical':
                    ratio = y / height
                else:
                    ratio = x / width
                
                # Smooth interpolation with easing
                eased_ratio = ratio * ratio * (3 - 2 * ratio)  # Smoothstep
                
                r = int(color1[0] * (1 - eased_ratio) + color2[0] * eased_ratio)
                g = int(color1[1] * (1 - eased_ratio) + color2[1] * eased_ratio)
                b = int(color1[2] * (1 - eased_ratio) + color2[2] * eased_ratio)
                
                # Add subtle noise for texture
                noise = random.randint(-3, 3)
                r = max(0, min(255, r + noise))
                g = max(0, min(255, g + noise))
                b = max(0, min(255, b + noise))
                
                pixels[x, y] = (r, g, b)
        
        # Add subtle radial gradient overlay for depth
        draw = ImageDraw.Draw(img, 'RGBA')
        center_x, center_y = width // 2, height // 2
        max_radius = int((width ** 2 + height ** 2) ** 0.5)
        
        # Create subtle vignette effect
        for radius in range(max_radius, 0, -10):
            alpha = int(5 * (1 - radius / max_radius))
            if alpha > 0:
                overlay = Image.new('RGBA', size, (0, 0, 0, alpha))
                mask = Image.new('L', size, 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse(
                    [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
                    fill=255
                )
                overlay.putalpha(mask)
                img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        if output_path is None:
            output_path = os.path.join(self.output_dir, "gradient_bg.jpg")
        
        img.save(output_path, 'JPEG', quality=98)
        return output_path
