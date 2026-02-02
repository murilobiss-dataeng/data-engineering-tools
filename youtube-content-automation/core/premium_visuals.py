"""
Premium Visual System for Salmo do Dia and spiritual content.

This module provides professional-grade visual generation including:
- Premium font management with Google Fonts support
- Sophisticated gradient backgrounds with vignette effects
- Animated particles and light effects
- Professional text rendering with hierarchy
- Decorative elements and frames
"""

import os
import math
import random
import hashlib
import urllib.request
from typing import Tuple, List, Optional, Dict
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np


# =============================================================================
# PROFESSIONAL COLOR PALETTES FOR SPIRITUAL CONTENT
# =============================================================================

SPIRITUAL_PALETTES = {
    "heavenly": {
        "name": "Celestial Dourado",
        "primary": (255, 215, 140),      # Dourado suave
        "secondary": (180, 150, 100),    # Bronze
        "accent": (255, 248, 220),       # Creme luminoso
        "bg_dark": (15, 12, 25),         # Azul noite profundo
        "bg_mid": (35, 28, 55),          # Roxo escuro
        "bg_light": (55, 45, 85),        # Lavanda escura
        "text_primary": (255, 252, 245), # Branco quente
        "text_secondary": (220, 200, 160), # Dourado claro
        "glow": (255, 230, 180, 60),     # Brilho dourado
    },
    "sacred": {
        "name": "Sagrado Azul",
        "primary": (100, 150, 220),      # Azul celeste
        "secondary": (70, 100, 160),     # Azul profundo
        "accent": (200, 220, 255),       # Azul claro
        "bg_dark": (10, 15, 30),         # Azul marinho escuro
        "bg_mid": (20, 30, 55),          # Azul noite
        "bg_light": (35, 50, 80),        # Azul médio
        "text_primary": (255, 255, 255), # Branco puro
        "text_secondary": (180, 200, 240), # Azul claro
        "glow": (150, 180, 255, 50),     # Brilho azul
    },
    "dawn": {
        "name": "Amanhecer",
        "primary": (255, 180, 120),      # Laranja suave
        "secondary": (200, 130, 90),     # Terra
        "accent": (255, 220, 180),       # Pêssego
        "bg_dark": (25, 15, 20),         # Marrom escuro
        "bg_mid": (50, 30, 40),          # Vinho escuro
        "bg_light": (80, 50, 60),        # Rosa escuro
        "text_primary": (255, 250, 240), # Branco creme
        "text_secondary": (255, 200, 160), # Pêssego claro
        "glow": (255, 200, 150, 55),     # Brilho quente
    },
    "serene": {
        "name": "Serenidade",
        "primary": (180, 200, 180),      # Verde sálvia
        "secondary": (120, 150, 120),    # Verde musgo
        "accent": (220, 235, 220),       # Verde claro
        "bg_dark": (15, 20, 18),         # Verde escuro
        "bg_mid": (30, 40, 35),          # Verde floresta
        "bg_light": (50, 65, 55),        # Verde médio
        "text_primary": (250, 255, 250), # Branco esverdeado
        "text_secondary": (200, 220, 200), # Verde claro
        "glow": (180, 220, 180, 45),     # Brilho verde
    },
}

# =============================================================================
# PREMIUM FONT MANAGEMENT
# =============================================================================

GOOGLE_FONTS = {
    "cinzel": {
        "name": "Cinzel",
        # URLs diretas do Google Fonts static
        "url_regular": "https://fonts.gstatic.com/s/cinzel/v23/8vIU7ww63mVu7gtR-kwKxNvkNOjw-tbnfY3lCQ.ttf",
        "url_bold": "https://fonts.gstatic.com/s/cinzel/v23/8vIU7ww63mVu7gtR-kwKxNvkNOjw-jDgfY3lCQ.ttf",
        "style": "elegant",
        "use_for": "titles"
    },
    "playfair": {
        "name": "Playfair Display",
        "url_regular": "https://fonts.gstatic.com/s/playfairdisplay/v37/nuFvD-vYSZviVYUb_rj3ij__anPXJzDwcbmjWBN2PKdFvXDXbtY.ttf",
        "url_bold": "https://fonts.gstatic.com/s/playfairdisplay/v37/nuFvD-vYSZviVYUb_rj3ij__anPXJzDwcbmjWBN2PKeiu3DXbtY.ttf",
        "style": "classic",
        "use_for": "titles"
    },
    "cormorant": {
        "name": "Cormorant Garamond",
        "url_regular": "https://fonts.gstatic.com/s/cormorantgaramond/v16/co3bmX5slCNuHLi8bLeY9MK7whWMhyjornFLsS6V7w.ttf",
        "url_bold": "https://fonts.gstatic.com/s/cormorantgaramond/v16/co3YmX5slCNuHLi8bLeY9MK7whWMhyjQAllvuQWJ5heb_w.ttf",
        "style": "spiritual",
        "use_for": "body"
    },
    "eb_garamond": {
        "name": "EB Garamond",
        "url_regular": "https://fonts.gstatic.com/s/ebgaramond/v27/SlGDmQSNjdsmc35JDF1K5E55YMjF_7DPuGi-6_RkC49_S6w.ttf",
        "url_bold": "https://fonts.gstatic.com/s/ebgaramond/v27/SlGDmQSNjdsmc35JDF1K5E55YMjF_7DPuGi-2fNkC49_S6w.ttf",
        "style": "biblical",
        "use_for": "body"
    },
    "lora": {
        "name": "Lora",
        "url_regular": "https://fonts.gstatic.com/s/lora/v35/0QI6MX1D_JOuGQbT0gvTJPa787weuxJBkq0.ttf",
        "url_bold": "https://fonts.gstatic.com/s/lora/v35/0QI6MX1D_JOuGQbT0gvTJPa787z5vBJBkq0.ttf",
        "style": "readable",
        "use_for": "body"
    },
}

# Fallback system fonts
SYSTEM_FONTS = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf',
    '/System/Library/Fonts/Times.ttc',
]


class FontManager:
    """Manages premium font downloading and loading."""
    
    def __init__(self, fonts_dir: str = "assets/fonts"):
        self.fonts_dir = fonts_dir
        os.makedirs(fonts_dir, exist_ok=True)
        self._font_cache: Dict[str, ImageFont.FreeTypeFont] = {}
    
    def download_font(self, font_key: str, bold: bool = False) -> Optional[str]:
        """Download a Google Font if not already cached."""
        if font_key not in GOOGLE_FONTS:
            return None
        
        font_info = GOOGLE_FONTS[font_key]
        url = font_info["url_bold"] if bold else font_info["url_regular"]
        suffix = "Bold" if bold else "Regular"
        filename = f"{font_info['name'].replace(' ', '')}_{suffix}.ttf"
        filepath = os.path.join(self.fonts_dir, filename)
        
        if os.path.exists(filepath):
            return filepath
        
        try:
            print(f"      → Baixando fonte {font_info['name']}...", flush=True)
            urllib.request.urlretrieve(url, filepath)
            return filepath
        except Exception as e:
            print(f"      ⚠ Não foi possível baixar {font_info['name']}: {e}")
            return None
    
    def get_font(self, font_key: str, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        """Get a font, downloading if necessary, with fallback to system fonts."""
        cache_key = f"{font_key}_{size}_{bold}"
        
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]
        
        # Try to download Google Font
        font_path = self.download_font(font_key, bold)
        
        if font_path and os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, size)
                self._font_cache[cache_key] = font
                return font
            except Exception:
                pass
        
        # Fallback to system fonts
        for sys_font in SYSTEM_FONTS:
            if os.path.exists(sys_font):
                try:
                    font = ImageFont.truetype(sys_font, size)
                    self._font_cache[cache_key] = font
                    return font
                except Exception:
                    continue
        
        # Ultimate fallback
        return ImageFont.load_default()
    
    def get_title_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Get the premium title font (Cinzel Bold)."""
        return self.get_font("cinzel", size, bold=True)
    
    def get_body_font(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        """Get the premium body font (EB Garamond)."""
        return self.get_font("eb_garamond", size, bold=bold)


# =============================================================================
# PREMIUM BACKGROUND GENERATOR
# =============================================================================

class PremiumBackgroundGenerator:
    """Generates professional-grade backgrounds for spiritual content."""
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def create_celestial_gradient(
        self,
        size: Tuple[int, int],
        palette_name: str = "heavenly",
        output_path: Optional[str] = None
    ) -> Image.Image:
        """Create a sophisticated multi-layer gradient with celestial feel."""
        palette = SPIRITUAL_PALETTES.get(palette_name, SPIRITUAL_PALETTES["heavenly"])
        width, height = size
        
        # Create base gradient (vertical)
        img = Image.new('RGB', size)
        pixels = img.load()
        
        for y in range(height):
            # Multi-stop gradient with smooth transitions
            ratio = y / height
            
            if ratio < 0.3:
                # Top section: dark to mid
                local_ratio = ratio / 0.3
                local_ratio = self._ease_in_out(local_ratio)
                color = self._interpolate_color(palette["bg_dark"], palette["bg_mid"], local_ratio)
            elif ratio < 0.7:
                # Middle section: mid gradient
                local_ratio = (ratio - 0.3) / 0.4
                local_ratio = self._ease_in_out(local_ratio)
                color = self._interpolate_color(palette["bg_mid"], palette["bg_light"], local_ratio)
            else:
                # Bottom section: light to mid
                local_ratio = (ratio - 0.7) / 0.3
                local_ratio = self._ease_in_out(local_ratio)
                color = self._interpolate_color(palette["bg_light"], palette["bg_mid"], local_ratio)
            
            for x in range(width):
                # Add subtle horizontal variation
                h_variation = math.sin(x / width * math.pi) * 0.05
                final_color = tuple(
                    max(0, min(255, int(c * (1 + h_variation))))
                    for c in color
                )
                pixels[x, y] = final_color
        
        # Add noise texture for depth
        img = self._add_subtle_noise(img, intensity=3)
        
        # Add radial light from top center
        img = self._add_divine_light(img, palette)
        
        # Add vignette
        img = self._add_vignette(img, strength=0.4)
        
        if output_path:
            img.save(output_path, 'JPEG', quality=98)
        
        return img
    
    def create_animated_background_frames(
        self,
        size: Tuple[int, int],
        duration: float,
        fps: int = 30,
        palette_name: str = "heavenly",
        output_dir: Optional[str] = None
    ) -> List[str]:
        """Generate frames for animated background with subtle movement."""
        palette = SPIRITUAL_PALETTES.get(palette_name, SPIRITUAL_PALETTES["heavenly"])
        total_frames = int(duration * fps)
        frame_paths = []
        
        if output_dir is None:
            output_dir = os.path.join(self.output_dir, "bg_frames")
        os.makedirs(output_dir, exist_ok=True)
        
        # Create base background once
        base_bg = self.create_celestial_gradient(size, palette_name)
        
        for frame_idx in range(total_frames):
            progress = frame_idx / total_frames
            
            # Clone base
            frame = base_bg.copy()
            
            # Add animated particles
            frame = self._add_floating_particles(
                frame, palette, progress, num_particles=15
            )
            
            # Add subtle light pulse
            pulse = 0.95 + 0.05 * math.sin(progress * 2 * math.pi)
            enhancer = ImageEnhance.Brightness(frame)
            frame = enhancer.enhance(pulse)
            
            # Save frame
            frame_path = os.path.join(output_dir, f"frame_{frame_idx:05d}.jpg")
            frame.save(frame_path, 'JPEG', quality=92)
            frame_paths.append(frame_path)
        
        return frame_paths
    
    def _ease_in_out(self, t: float) -> float:
        """Smooth easing function."""
        return t * t * (3 - 2 * t)
    
    def _interpolate_color(
        self,
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int],
        ratio: float
    ) -> Tuple[int, int, int]:
        """Interpolate between two colors."""
        return tuple(
            int(color1[i] * (1 - ratio) + color2[i] * ratio)
            for i in range(3)
        )
    
    def _add_subtle_noise(self, img: Image.Image, intensity: int = 3) -> Image.Image:
        """Add subtle noise for texture."""
        arr = np.array(img, dtype=np.int16)
        noise = np.random.randint(-intensity, intensity + 1, arr.shape, dtype=np.int16)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(arr)
    
    def _add_divine_light(
        self,
        img: Image.Image,
        palette: Dict,
        position: Tuple[float, float] = (0.5, 0.1)
    ) -> Image.Image:
        """Add a soft divine light effect from the top."""
        width, height = img.size
        
        # Create light overlay
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        center_x = int(width * position[0])
        center_y = int(height * position[1])
        max_radius = int(max(width, height) * 0.8)
        
        glow_color = palette.get("glow", (255, 230, 180, 60))
        
        # Draw concentric circles with decreasing alpha
        for r in range(max_radius, 0, -5):
            alpha = int(glow_color[3] * (1 - r / max_radius) ** 2)
            color = (*glow_color[:3], alpha)
            draw.ellipse(
                [center_x - r, center_y - r, center_x + r, center_y + r],
                fill=color
            )
        
        # Apply gaussian blur for smoothness
        overlay = overlay.filter(ImageFilter.GaussianBlur(radius=50))
        
        # Composite
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        return img.convert('RGB')
    
    def _add_vignette(self, img: Image.Image, strength: float = 0.4) -> Image.Image:
        """Add a professional vignette effect."""
        width, height = img.size
        
        # Create vignette mask
        vignette = Image.new('L', (width, height), 255)
        draw = ImageDraw.Draw(vignette)
        
        # Calculate ellipse dimensions
        center_x, center_y = width // 2, height // 2
        max_dist = math.sqrt(center_x**2 + center_y**2)
        
        for y in range(height):
            for x in range(width):
                # Distance from center (normalized)
                dist = math.sqrt((x - center_x)**2 + (y - center_y)**2) / max_dist
                # Smooth falloff
                factor = 1 - (dist ** 2) * strength
                factor = max(0.3, min(1.0, factor))
                vignette.putpixel((x, y), int(255 * factor))
        
        # Apply blur for smoothness
        vignette = vignette.filter(ImageFilter.GaussianBlur(radius=30))
        
        # Apply vignette to image
        img = img.convert('RGB')
        result = Image.new('RGB', (width, height))
        
        for y in range(height):
            for x in range(width):
                v = vignette.getpixel((x, y)) / 255
                original = img.getpixel((x, y))
                result.putpixel((x, y), tuple(int(c * v) for c in original))
        
        return result
    
    def _add_floating_particles(
        self,
        img: Image.Image,
        palette: Dict,
        progress: float,
        num_particles: int = 20
    ) -> Image.Image:
        """Add floating light particles for animated backgrounds."""
        width, height = img.size
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        glow_color = palette.get("glow", (255, 230, 180, 60))
        
        # Use deterministic seed based on frame for consistency
        random.seed(42)
        
        for i in range(num_particles):
            # Particle properties (deterministic per particle)
            base_x = random.random()
            base_y = random.random()
            speed = 0.0005 + random.random() * 0.001
            size = 2 + random.random() * 4
            phase = random.random() * 2 * math.pi
            
            # Calculate position with gentle floating motion
            x = int(width * (base_x + 0.02 * math.sin(progress * 2 * math.pi + phase)))
            y = int(height * (base_y - speed * progress * 100) % 1)  # Slowly rise
            
            # Particle brightness varies
            brightness = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(progress * 4 * math.pi + phase))
            alpha = int(glow_color[3] * brightness)
            
            # Draw particle with soft glow
            for r in range(int(size * 3), 0, -1):
                a = int(alpha * (1 - r / (size * 3)) ** 2)
                color = (*glow_color[:3], a)
                draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
        
        random.seed()  # Reset random seed
        
        # Blur for soft glow
        overlay = overlay.filter(ImageFilter.GaussianBlur(radius=3))
        
        img = img.convert('RGBA')
        return Image.alpha_composite(img, overlay).convert('RGB')


# =============================================================================
# PREMIUM TEXT RENDERER
# =============================================================================

class PremiumTextRenderer:
    """Renders professional text with hierarchy, shadows, and effects."""
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        self.font_manager = FontManager(os.path.join(output_dir, "fonts"))
        os.makedirs(output_dir, exist_ok=True)
    
    def render_psalm_text(
        self,
        title: str,
        verses: str,
        size: Tuple[int, int],
        palette_name: str = "heavenly",
        is_shorts: bool = True
    ) -> Image.Image:
        """Render psalm text with professional typography."""
        palette = SPIRITUAL_PALETTES.get(palette_name, SPIRITUAL_PALETTES["heavenly"])
        width, height = size
        
        # Create transparent image
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate sizes based on video format
        if is_shorts:
            title_size = int(height * 0.045)  # ~86px for 1920 height
            verse_size = int(height * 0.032)  # ~61px for 1920 height
            padding = int(width * 0.08)
            line_spacing = 1.6
        else:
            title_size = int(height * 0.065)  # ~70px for 1080 height
            verse_size = int(height * 0.042)  # ~45px for 1080 height
            padding = int(width * 0.06)
            line_spacing = 1.5
        
        # Get fonts
        title_font = self.font_manager.get_title_font(title_size)
        verse_font = self.font_manager.get_body_font(verse_size)
        
        # Calculate text area
        max_width = width - (padding * 2)
        current_y = int(height * 0.15) if is_shorts else int(height * 0.12)
        
        # Render title with glow effect
        title_color = palette["text_primary"]
        glow_color = (*palette["primary"][:3], 80)
        
        # Draw title glow (multiple passes)
        for offset in range(8, 0, -2):
            alpha = int(30 * (1 - offset / 8))
            glow = (*palette["primary"][:3], alpha)
            self._draw_text_centered(
                draw, title, title_font, current_y,
                width, glow, offset_blur=offset
            )
        
        # Draw title shadow
        shadow_color = (0, 0, 0, 100)
        self._draw_text_centered(
            draw, title, title_font, current_y + 4,
            width, shadow_color
        )
        
        # Draw title
        self._draw_text_centered(
            draw, title, title_font, current_y,
            width, title_color
        )
        
        # Calculate title height
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        current_y += (title_bbox[3] - title_bbox[1]) + int(height * 0.05)
        
        # Add decorative separator
        self._draw_separator(draw, current_y, width, palette)
        current_y += int(height * 0.04)
        
        # Render verses
        verse_color = palette["text_secondary"]
        verse_lines = self._wrap_text(verses, verse_font, max_width, draw)
        
        for line in verse_lines:
            if not line.strip():
                current_y += int(verse_size * 0.5)
                continue
            
            # Draw verse shadow
            self._draw_text_centered(
                draw, line, verse_font, current_y + 2,
                width, (0, 0, 0, 60)
            )
            
            # Draw verse
            self._draw_text_centered(
                draw, line, verse_font, current_y,
                width, verse_color
            )
            
            current_y += int(verse_size * line_spacing)
            
            # Check if we're running out of space
            if current_y > height * 0.88:
                break
        
        return img
    
    def _draw_text_centered(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.FreeTypeFont,
        y: int,
        width: int,
        color: Tuple,
        offset_blur: int = 0
    ):
        """Draw text centered horizontally."""
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        
        if offset_blur > 0:
            # Draw with slight offset for blur effect
            for dx in [-offset_blur, 0, offset_blur]:
                for dy in [-offset_blur, 0, offset_blur]:
                    draw.text((x + dx, y + dy), text, font=font, fill=color)
        else:
            draw.text((x, y), text, font=font, fill=color)
    
    def _draw_separator(
        self,
        draw: ImageDraw.ImageDraw,
        y: int,
        width: int,
        palette: Dict
    ):
        """Draw a decorative separator line."""
        line_width = int(width * 0.3)
        x_start = (width - line_width) // 2
        x_end = x_start + line_width
        
        # Gradient line with fade at edges
        for x in range(x_start, x_end):
            progress = (x - x_start) / line_width
            # Fade at edges
            alpha = int(100 * (1 - abs(progress - 0.5) * 2) ** 2)
            color = (*palette["primary"][:3], alpha)
            draw.line([(x, y), (x, y + 2)], fill=color)
        
        # Center ornament (diamond)
        center_x = width // 2
        ornament_size = 6
        draw.polygon([
            (center_x, y - ornament_size),
            (center_x + ornament_size, y),
            (center_x, y + ornament_size),
            (center_x - ornament_size, y)
        ], fill=(*palette["primary"][:3], 150))
    
    def _wrap_text(
        self,
        text: str,
        font: ImageFont.FreeTypeFont,
        max_width: int,
        draw: ImageDraw.ImageDraw
    ) -> List[str]:
        """Wrap text to fit within max width."""
        lines = []
        paragraphs = text.split('\n')
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                lines.append('')
                continue
            
            words = paragraph.split()
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = draw.textbbox((0, 0), test_line, font=font)
                
                if bbox[2] - bbox[0] <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
        
        return lines


# =============================================================================
# PREMIUM VIDEO COMPOSITOR
# =============================================================================

class PremiumVideoCompositor:
    """Composes premium video frames with all visual elements."""
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        self.bg_generator = PremiumBackgroundGenerator(output_dir)
        self.text_renderer = PremiumTextRenderer(output_dir)
        os.makedirs(output_dir, exist_ok=True)
    
    def create_psalm_frame(
        self,
        title: str,
        verses: str,
        size: Tuple[int, int],
        palette_name: str = "heavenly",
        is_shorts: bool = True,
        frame_progress: float = 0.0
    ) -> Image.Image:
        """Create a single premium frame for psalm video."""
        # Create background
        bg = self.bg_generator.create_celestial_gradient(size, palette_name)
        
        # Add subtle animated particles (based on progress)
        palette = SPIRITUAL_PALETTES.get(palette_name, SPIRITUAL_PALETTES["heavenly"])
        bg = self.bg_generator._add_floating_particles(bg, palette, frame_progress, num_particles=12)
        
        # Render text overlay
        text_overlay = self.text_renderer.render_psalm_text(
            title, verses, size, palette_name, is_shorts
        )
        
        # Composite
        bg = bg.convert('RGBA')
        result = Image.alpha_composite(bg, text_overlay)
        
        return result.convert('RGB')
    
    def create_static_background(
        self,
        size: Tuple[int, int],
        palette_name: str = "heavenly",
        output_path: Optional[str] = None
    ) -> str:
        """Create a static premium background image."""
        bg = self.bg_generator.create_celestial_gradient(size, palette_name)
        
        if output_path is None:
            output_path = os.path.join(self.output_dir, f"premium_bg_{palette_name}.jpg")
        
        bg.save(output_path, 'JPEG', quality=98)
        return output_path
    
    def create_psalm_video_frames(
        self,
        title: str,
        verses: str,
        duration: float,
        size: Tuple[int, int],
        fps: int = 30,
        palette_name: str = "heavenly",
        is_shorts: bool = True,
        output_dir: Optional[str] = None
    ) -> List[str]:
        """Generate all frames for a psalm video."""
        total_frames = int(duration * fps)
        
        if output_dir is None:
            output_dir = os.path.join(self.output_dir, "psalm_frames")
        os.makedirs(output_dir, exist_ok=True)
        
        frame_paths = []
        
        # Pre-render static elements
        bg_base = self.bg_generator.create_celestial_gradient(size, palette_name)
        text_overlay = self.text_renderer.render_psalm_text(
            title, verses, size, palette_name, is_shorts
        )
        
        palette = SPIRITUAL_PALETTES.get(palette_name, SPIRITUAL_PALETTES["heavenly"])
        
        print(f"      → Gerando {total_frames} frames de alta qualidade...", flush=True)
        
        for frame_idx in range(total_frames):
            progress = frame_idx / total_frames
            
            # Clone base background
            frame = bg_base.copy()
            
            # Add animated particles
            frame = self.bg_generator._add_floating_particles(
                frame, palette, progress, num_particles=12
            )
            
            # Add subtle brightness pulse
            pulse = 0.97 + 0.03 * math.sin(progress * 2 * math.pi)
            enhancer = ImageEnhance.Brightness(frame)
            frame = enhancer.enhance(pulse)
            
            # Composite text
            frame = frame.convert('RGBA')
            frame = Image.alpha_composite(frame, text_overlay)
            
            # Save frame
            frame_path = os.path.join(output_dir, f"frame_{frame_idx:05d}.jpg")
            frame.convert('RGB').save(frame_path, 'JPEG', quality=92)
            frame_paths.append(frame_path)
            
            # Progress indicator every 10%
            if frame_idx % (total_frames // 10) == 0:
                pct = int(frame_idx / total_frames * 100)
                print(f"        {pct}% completo...", flush=True)
        
        return frame_paths


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_palette_for_mood(mood: str = "peaceful") -> str:
    """Get the best palette for a given mood."""
    mood_mapping = {
        "peaceful": "heavenly",
        "powerful": "sacred",
        "hopeful": "dawn",
        "calm": "serene",
        "protection": "sacred",
        "guidance": "heavenly",
        "trust": "serene",
        "praise": "dawn",
    }
    return mood_mapping.get(mood.lower(), "heavenly")


def analyze_psalm_mood(psalm_text: str) -> str:
    """Analyze psalm text to determine the best visual mood."""
    text_lower = psalm_text.lower()
    
    if any(word in text_lower for word in ["proteção", "proteger", "escudo", "refúgio", "fortaleza"]):
        return "sacred"
    elif any(word in text_lower for word in ["luz", "manhã", "amanhecer", "alegria", "louvor"]):
        return "dawn"
    elif any(word in text_lower for word in ["paz", "descanso", "pastos", "águas tranquilas", "repouso"]):
        return "serene"
    else:
        return "heavenly"
