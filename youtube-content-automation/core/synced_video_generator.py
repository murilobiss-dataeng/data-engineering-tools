"""
Synced Video Generator - Gera vídeos com texto sincronizado ao áudio.

Cada verso/página é exibido enquanto está sendo narrado.
O sistema calcula automaticamente o tempo de cada página baseado no áudio.
"""

import os
import math
import shutil
from typing import List, Dict, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np

from moviepy.editor import (
    ImageClip, CompositeVideoClip, AudioFileClip,
    concatenate_videoclips, ImageSequenceClip
)


class SyncedVideoGenerator:
    """Gera vídeos com texto sincronizado ao áudio."""
    
    # Dimensões padrão
    SHORTS_SIZE = (1080, 1920)  # 9:16 vertical
    LONG_FORM_SIZE = (1920, 1080)  # 16:9 horizontal
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self._font_manager = None
        self._bg_generator = None
    
    @property
    def font_manager(self):
        """Lazy load font manager."""
        if self._font_manager is None:
            from core.premium_visuals import FontManager
            self._font_manager = FontManager(os.path.join(self.output_dir, "fonts"))
        return self._font_manager
    
    @property
    def bg_generator(self):
        """Lazy load background generator."""
        if self._bg_generator is None:
            from core.premium_visuals import PremiumBackgroundGenerator
            self._bg_generator = PremiumBackgroundGenerator(self.output_dir)
        return self._bg_generator
    
    def split_into_pages(
        self,
        text: str,
        max_lines_per_page: int = 4,
        max_chars_per_line: int = 40
    ) -> List[str]:
        """
        Divide o texto em páginas para exibição.
        
        Args:
            text: Texto completo do salmo
            max_lines_per_page: Máximo de linhas por página
            max_chars_per_line: Máximo de caracteres por linha (para wrap)
            
        Returns:
            Lista de páginas (cada página é uma string)
        """
        # Separa por linhas (versos)
        lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
        
        pages = []
        current_page = []
        
        for line in lines:
            # Se a linha é muito longa, pode ocupar mais espaço visual
            visual_lines = math.ceil(len(line) / max_chars_per_line)
            
            # Verifica se adicionar esta linha excede o limite
            current_visual_lines = sum(
                math.ceil(len(l) / max_chars_per_line) for l in current_page
            )
            
            if current_visual_lines + visual_lines > max_lines_per_page and current_page:
                # Salva a página atual e começa uma nova
                pages.append('\n'.join(current_page))
                current_page = [line]
            else:
                current_page.append(line)
        
        # Adiciona a última página
        if current_page:
            pages.append('\n'.join(current_page))
        
        return pages
    
    def calculate_page_durations(
        self,
        pages: List[str],
        total_duration: float,
        min_page_duration: float = 3.0
    ) -> List[float]:
        """
        Calcula a duração de cada página baseado no tamanho do texto.
        
        Args:
            pages: Lista de páginas
            total_duration: Duração total do áudio
            min_page_duration: Duração mínima por página
            
        Returns:
            Lista de durações para cada página
        """
        # Calcula peso de cada página baseado no número de caracteres
        weights = [len(page) for page in pages]
        total_weight = sum(weights)
        
        # Distribui o tempo proporcionalmente
        durations = []
        for weight in weights:
            proportion = weight / total_weight
            duration = max(min_page_duration, total_duration * proportion)
            durations.append(duration)
        
        # Normaliza para garantir que a soma seja igual ao total
        duration_sum = sum(durations)
        scale = total_duration / duration_sum
        durations = [d * scale for d in durations]
        
        return durations
    
    def create_page_frame(
        self,
        title: str,
        page_text: str,
        page_number: int,
        total_pages: int,
        size: Tuple[int, int],
        palette_name: str = "heavenly",
        is_shorts: bool = True
    ) -> Image.Image:
        """
        Cria um frame para uma página do salmo.
        
        Args:
            title: Título do salmo (ex: "Salmo 23")
            page_text: Texto da página atual
            page_number: Número da página (0-based)
            total_pages: Total de páginas
            size: Tamanho da imagem (width, height)
            palette_name: Nome da paleta de cores
            is_shorts: Se é formato shorts (vertical)
            
        Returns:
            Imagem PIL da página
        """
        from core.premium_visuals import SPIRITUAL_PALETTES
        
        palette = SPIRITUAL_PALETTES.get(palette_name, SPIRITUAL_PALETTES["heavenly"])
        width, height = size
        
        # Cria background
        bg = self.bg_generator.create_celestial_gradient(size, palette_name)
        
        # Adiciona partículas estáticas (efeito sutil)
        bg = self._add_static_particles(bg, palette, page_number)
        
        # Cria overlay de texto
        img = bg.convert('RGBA')
        draw = ImageDraw.Draw(img)
        
        # Configurações de tipografia baseadas no formato
        if is_shorts:
            title_size = int(height * 0.04)
            verse_size = int(height * 0.035)
            padding = int(width * 0.08)
            line_spacing = 1.8
            title_y = int(height * 0.08)
        else:
            title_size = int(height * 0.055)
            verse_size = int(height * 0.045)
            padding = int(width * 0.08)
            line_spacing = 1.6
            title_y = int(height * 0.08)
        
        # Fontes
        title_font = self.font_manager.get_title_font(title_size)
        verse_font = self.font_manager.get_body_font(verse_size)
        
        max_width = width - (padding * 2)
        
        # Desenha título com glow
        title_color = palette["text_primary"]
        self._draw_text_with_glow(
            draw, title, title_font, title_y,
            width, title_color, palette["primary"]
        )
        
        # Desenha indicador de página (ex: "1/5")
        page_indicator = f"{page_number + 1}/{total_pages}"
        indicator_font = self.font_manager.get_body_font(int(verse_size * 0.6))
        indicator_y = title_y + title_size + int(height * 0.02)
        self._draw_text_centered(
            draw, page_indicator, indicator_font, indicator_y,
            width, (*palette["text_secondary"][:3], 150)
        )
        
        # Desenha separador
        sep_y = indicator_y + int(height * 0.03)
        self._draw_separator(draw, sep_y, width, palette)
        
        # Desenha versos
        verse_start_y = sep_y + int(height * 0.04)
        verse_color = palette["text_primary"]
        
        # Wrap e desenha cada linha do texto
        wrapped_lines = self._wrap_text(page_text, verse_font, max_width, draw)
        current_y = verse_start_y
        
        for line in wrapped_lines:
            if not line.strip():
                current_y += int(verse_size * 0.5)
                continue
            
            # Sombra suave
            self._draw_text_centered(
                draw, line, verse_font, current_y + 3,
                width, (0, 0, 0, 80)
            )
            
            # Texto
            self._draw_text_centered(
                draw, line, verse_font, current_y,
                width, verse_color
            )
            
            current_y += int(verse_size * line_spacing)
        
        return img.convert('RGB')
    
    def _add_static_particles(
        self,
        img: Image.Image,
        palette: Dict,
        seed: int = 0
    ) -> Image.Image:
        """Adiciona partículas de luz estáticas."""
        import random
        random.seed(42 + seed)  # Determinístico por página
        
        width, height = img.size
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        glow_color = palette.get("glow", (255, 230, 180, 60))
        
        for _ in range(8):
            x = int(random.random() * width)
            y = int(random.random() * height)
            size = 2 + random.random() * 3
            alpha = int(glow_color[3] * (0.3 + 0.7 * random.random()))
            
            for r in range(int(size * 3), 0, -1):
                a = int(alpha * (1 - r / (size * 3)) ** 2)
                color = (*glow_color[:3], a)
                draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
        
        random.seed()
        
        overlay = overlay.filter(ImageFilter.GaussianBlur(radius=2))
        img = img.convert('RGBA')
        return Image.alpha_composite(img, overlay).convert('RGB')
    
    def _draw_text_with_glow(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.FreeTypeFont,
        y: int,
        width: int,
        color: Tuple,
        glow_color: Tuple
    ):
        """Desenha texto com efeito de glow."""
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        
        # Glow
        for offset in range(6, 0, -2):
            alpha = int(40 * (1 - offset / 6))
            glow = (*glow_color[:3], alpha)
            for dx in [-offset, 0, offset]:
                for dy in [-offset, 0, offset]:
                    draw.text((x + dx, y + dy), text, font=font, fill=glow)
        
        # Sombra
        draw.text((x + 3, y + 3), text, font=font, fill=(0, 0, 0, 100))
        
        # Texto
        draw.text((x, y), text, font=font, fill=color)
    
    def _draw_text_centered(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.FreeTypeFont,
        y: int,
        width: int,
        color: Tuple
    ):
        """Desenha texto centralizado."""
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y), text, font=font, fill=color)
    
    def _draw_separator(
        self,
        draw: ImageDraw.ImageDraw,
        y: int,
        width: int,
        palette: Dict
    ):
        """Desenha separador decorativo."""
        line_width = int(width * 0.25)
        x_start = (width - line_width) // 2
        x_end = x_start + line_width
        
        for x in range(x_start, x_end):
            progress = (x - x_start) / line_width
            alpha = int(80 * (1 - abs(progress - 0.5) * 2) ** 2)
            color = (*palette["primary"][:3], alpha)
            draw.line([(x, y), (x, y + 2)], fill=color)
        
        # Diamante central
        center_x = width // 2
        size = 5
        draw.polygon([
            (center_x, y - size),
            (center_x + size, y),
            (center_x, y + size),
            (center_x - size, y)
        ], fill=(*palette["primary"][:3], 120))
    
    def _wrap_text(
        self,
        text: str,
        font: ImageFont.FreeTypeFont,
        max_width: int,
        draw: ImageDraw.ImageDraw
    ) -> List[str]:
        """Quebra texto para caber na largura máxima."""
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
    
    def create_synced_video(
        self,
        title: str,
        full_text: str,
        audio_path: str,
        output_filename: str,
        is_shorts: bool = True,
        palette: str = "heavenly",
        max_lines_per_page: int = 4,
        fps: int = 30
    ) -> str:
        """
        Cria vídeo com texto sincronizado ao áudio.
        
        Args:
            title: Título do salmo
            full_text: Texto completo do salmo
            audio_path: Caminho do arquivo de áudio
            output_filename: Nome do arquivo de saída
            is_shorts: Se é formato shorts (vertical)
            palette: Nome da paleta de cores
            max_lines_per_page: Máximo de linhas por página
            fps: Frames por segundo
            
        Returns:
            Caminho do vídeo gerado
        """
        size = self.SHORTS_SIZE if is_shorts else self.LONG_FORM_SIZE
        
        # Carrega áudio
        audio_clip = AudioFileClip(audio_path)
        total_duration = audio_clip.duration
        
        # Divide em páginas
        pages = self.split_into_pages(full_text, max_lines_per_page)
        total_pages = len(pages)
        
        print(f"      → Salmo dividido em {total_pages} páginas", flush=True)
        
        # Calcula duração de cada página
        durations = self.calculate_page_durations(pages, total_duration)
        
        # Gera clips de cada página
        video_clips = []
        
        for i, (page_text, duration) in enumerate(zip(pages, durations)):
            print(f"      → Gerando página {i+1}/{total_pages} ({duration:.1f}s)...", flush=True)
            
            # Cria frame para esta página
            frame = self.create_page_frame(
                title=title,
                page_text=page_text,
                page_number=i,
                total_pages=total_pages,
                size=size,
                palette_name=palette,
                is_shorts=is_shorts
            )
            
            # Converte para clip
            frame_array = np.array(frame)
            clip = ImageClip(frame_array, duration=duration)
            video_clips.append(clip)
        
        # Concatena todos os clips
        print(f"      → Concatenando {total_pages} páginas...", flush=True)
        final_video = concatenate_videoclips(video_clips, method="compose")
        final_video = final_video.set_audio(audio_clip)
        
        # Exporta
        output_path = os.path.join(self.output_dir, output_filename)
        video_type = "Short" if is_shorts else "Long-form"
        
        print(f"      → Codificando {video_type} ({output_filename})...", flush=True)
        
        final_video.write_videofile(
            output_path,
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            bitrate='10000k',
            audio_bitrate='192k',
            preset='medium',
            threads=4,
            logger='bar'
        )
        
        # Cleanup
        audio_clip.close()
        final_video.close()
        for clip in video_clips:
            clip.close()
        
        return output_path


def create_synced_salmo_video(
    salmo_nome: str,
    salmo_texto: str,
    audio_path: str,
    output_dir: str = "outputs",
    is_shorts: bool = True,
    palette: str = "heavenly"
) -> str:
    """
    Função auxiliar para criar vídeo de salmo sincronizado.
    
    Args:
        salmo_nome: Nome do salmo (ex: "Salmo 23")
        salmo_texto: Texto completo do salmo
        audio_path: Caminho do áudio
        output_dir: Diretório de saída
        is_shorts: Se é formato shorts
        palette: Paleta de cores
        
    Returns:
        Caminho do vídeo gerado
    """
    from datetime import datetime
    
    generator = SyncedVideoGenerator(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    format_suffix = "short" if is_shorts else "long"
    filename = f"salmo_synced_{format_suffix}_{timestamp}.mp4"
    
    return generator.create_synced_video(
        title=salmo_nome,
        full_text=salmo_texto,
        audio_path=audio_path,
        output_filename=filename,
        is_shorts=is_shorts,
        palette=palette,
        max_lines_per_page=4 if is_shorts else 5
    )
