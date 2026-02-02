"""Image processing utilities for video generation."""

import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from typing import Tuple, Optional, List
import requests
from io import BytesIO

# Cores para overlays e gradientes profissionais
PALETTES = {
    "blue_pro": ((15, 32, 72), (45, 95, 180), (120, 160, 220)),
    "warm": ((72, 32, 15), (180, 95, 45), (220, 160, 120)),
    "nature": ((20, 60, 40), (60, 120, 80), (140, 180, 150)),
    "elegant": ((40, 35, 55), (90, 80, 120), (160, 150, 190)),
    "energy": ((80, 30, 50), (160, 60, 100), (220, 140, 180)),
}


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
        
        # Vignette suave via numpy (se disponível) ou skip para performance
        
        if output_path is None:
            output_path = os.path.join(self.output_dir, "gradient_bg.jpg")

        img.save(output_path, 'JPEG', quality=98)
        return output_path

    def create_professional_background(
        self,
        size: Tuple[int, int],
        keyword: Optional[str] = None,
        palette: str = "blue_pro",
        output_path: Optional[str] = None
    ) -> str:
        """
        Cria background profissional: Leonardo.ai > Unsplash > gradiente.
        """
        out = output_path or os.path.join(self.output_dir, "bg_professional.jpg")
        prompt_keyword = (keyword or "professional").replace(",", " ")

        # 1. Leonardo.ai (imagens geradas por IA)
        try:
            from data_sources.leonardo_api import LeonardoAPI
            api = LeonardoAPI()
            if api.api_key:
                prompt = f"Professional background image for video, {prompt_keyword}, high quality, cinematic lighting, 16:9 aspect ratio, no text, no watermark"
                path = api.generate_and_save(prompt, out, size=size)
                if path:
                    img = Image.open(path).convert('RGB').resize(size, Image.Resampling.LANCZOS)
                    overlay = Image.new('RGBA', size, (0, 0, 0, 90))
                    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
                    img.save(out, 'JPEG', quality=95)
                    return out
        except Exception:
            pass

        # 2. Unsplash (fotos reais)
        if keyword:
            try:
                from data_sources.unsplash_api import UnsplashAPI
                unsplash = UnsplashAPI()
                photo_path = unsplash.search_photo(keyword, size=size, output_dir=self.output_dir)
                if photo_path:
                    img = Image.open(photo_path).convert('RGB').resize(size, Image.Resampling.LANCZOS)
                    overlay = Image.new('RGBA', size, (0, 0, 0, 110))
                    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
                    img.save(out, 'JPEG', quality=95)
                    return out
            except Exception:
                pass

        # 3. Gradiente (fallback)
        colors = PALETTES.get(palette, PALETTES["blue_pro"])
        return self.create_gradient_background(size, colors[0], colors[-1], out)
