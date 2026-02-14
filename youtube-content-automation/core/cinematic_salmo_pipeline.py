"""
Pipeline cinematográfico profissional para Salmo do Dia.

Foco: retenção e impacto imediato.
- Hook nos primeiros 1–2s, sem introdução lenta
- 4 frames: Hook (3s) → Continuação (4s) → Conclusão (4s) → Referência (2–3s)
- Duração total alvo: 25–35s (YouTube Shorts)
- Backgrounds EXCLUSIVAMENTE da pasta assets/
- Narração: exclusivamente edge-tts (pt-BR-ThalitaMultilingualNeural)
"""

import os
import logging
import time
from pathlib import Path
from typing import Tuple, Optional, List, Sequence, Dict, Any

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

WIDTH, HEIGHT = 1080, 1920
FPS = 30
ASSETS_DIR_DEFAULT = "assets"

# Cores retenção: branco quente, máximo contraste
TEXT_WARM_WHITE = (245, 242, 232, 255)  # #F5F2E8
SHADOW_RGBA = (0, 0, 0, 180)
GLOW_RGBA = (255, 248, 230, 80)

# Durações por frame (segundos) – referência fixa no fim
DURATION_HOOK = 3.0
DURATION_PART2 = 4.0
DURATION_PART3 = 4.0
DURATION_REFERENCE = 2.5
REFERENCE_FRAME_DURATION = DURATION_REFERENCE

# Densidade de texto: 10–16 palavras por frame (narrativa contínua, sem telas vazias)
PHRASE_MIN_WORDS = 10
PHRASE_MAX_WORDS = 16
REFERENCE_FRAME_DURATION_SYNC = 2.5
# Tempo mínimo de leitura por trecho (evita texto sumir rápido demais)
MIN_SEGMENT_DURATION = 1.0
# Transição cinematográfica: crossfade suave (nunca corte seco)
CROSSFADE_DURATION = 0.6

# Header fixo: referência bíblica no topo em todos os frames (identidade visual)
HEADER_HEIGHT = int(HEIGHT * 0.105)  # ~202px, legível em mobile

# Área do verso (camada 3): caixa fixa, margens simétricas, safe area mobile
VERSE_PADDING_H = int(WIDTH * 0.14)  # margens laterais generosas (editorial)
VERSE_PADDING_TOP = int(HEIGHT * 0.07)
VERSE_PADDING_BOTTOM = int(HEIGHT * 0.09)
VERSE_AREA_TOP = HEADER_HEIGHT + VERSE_PADDING_TOP
VERSE_AREA_BOTTOM = HEIGHT - VERSE_PADDING_BOTTOM
VERSE_AREA_HEIGHT = VERSE_AREA_BOTTOM - VERSE_AREA_TOP
VERSE_MAX_LINE_WIDTH = WIDTH - 2 * VERSE_PADDING_H
# Tipografia cinematográfica: respirável, elegante (nunca cortar palavras/sílabas)
VERSE_LINE_HEIGHT_RATIO = 0.078  # espaço entre linhas (ritmo visual)
VERSE_MIN_LINE_WIDTH_RATIO = 0.28  # evita orphan (linha última muito curta)

__all__ = [
    "load_background",
    "generate_voice",
    "get_forced_alignment",
    "segment_into_phrases",
    "render_phrase_overlay",
    "render_verse_only_overlay",
    "render_text_overlay",
    "render_retention_frame",
    "split_script_for_retention",
    "compose_video",
    "compose_retention_video",
    "compose_synced_video",
    "run_cinematic_salmo_pipeline",
]


# =============================================================================
# 1. LOAD BACKGROUND
# =============================================================================

def load_background(assets_dir: Optional[str] = None) -> Image.Image:
    """
    Carrega o background mais adequado da pasta assets/.
    Usa EXCLUSIVAMENTE imagens locais. Preferência: salmo_do_dia*.jpg.
    Redimensiona e recorta para 1080x1920 (vertical) mantendo aspecto.
    
    Raises:
        FileNotFoundError: Se não houver imagens em assets/
    """
    assets_path = Path(assets_dir or ASSETS_DIR_DEFAULT)
    if not assets_path.is_absolute():
        base = Path(__file__).resolve().parents[1]
        assets_path = base / assets_path
    if not assets_path.exists():
        raise FileNotFoundError(f"Pasta de assets não encontrada: {assets_path}")

    # Preferir imagens do salmo (salmo_do_dia*.jpg)
    candidates: List[Path] = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
        for f in sorted(assets_path.glob(ext)):
            if "salmo" in f.name.lower():
                candidates.insert(0, f)
            elif f.name != "curiosidade_do_dia.jpg" and f.name != "placar_do_dia.jpg":
                candidates.append(f)
    if not candidates:
        for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
            candidates.extend(sorted(assets_path.glob(ext)))
    if not candidates:
        raise FileNotFoundError(
            f"Nenhuma imagem encontrada em {assets_path}. "
            "Adicione imagens (ex: salmo_do_dia.jpg) em assets/."
        )

    chosen = candidates[0]
    logger.info("[1/6] Background selecionado: %s", chosen.name)
    img = Image.open(chosen).convert("RGB")

    # Crop/resize para 1080x1920 (vertical) – center crop depois scale
    w, h = img.size
    target_ratio = WIDTH / HEIGHT
    current_ratio = w / h
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    return img


def _apply_spiritual_grading(img: Image.Image) -> Image.Image:
    """Color grading espiritual: leve aquecimento, contraste suave, brilho sutil."""
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Color(img).enhance(1.1)
    img = ImageEnhance.Brightness(img).enhance(0.98)
    # Leve tom âmbar
    r, g, b = img.split()
    r = r.point(lambda x: min(255, int(x * 1.02)))
    b = b.point(lambda x: max(0, int(x * 0.98)))
    img = Image.merge("RGB", (r, g, b))
    return img


def _apply_soft_glow(img: Image.Image, radius: int = 25, strength: float = 0.15) -> Image.Image:
    """Adiciona glow suave (blur leve nas altas luzes)."""
    blurred = img.filter(ImageFilter.GaussianBlur(radius=radius))
    return Image.blend(img, blurred, strength)


def _apply_dark_cinematic_grading(img: Image.Image, vignette_strength: float = 0.5) -> Image.Image:
    """Dark cinematic: escurece, vignette, gradiente central escuro. Fundo nunca compete com texto."""
    img = ImageEnhance.Brightness(img).enhance(0.5)
    img = ImageEnhance.Contrast(img).enhance(1.15)
    w, h = img.size
    # Vignette suave
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = w // 2, h // 2
    max_r = (cx**2 + cy**2) ** 0.5
    for y in range(0, h, 8):
        for x in range(0, w, 8):
            r = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            alpha = int(255 * vignette_strength * (1 - (1 - r / max_r) ** 2))
            overlay.putpixel((x, y), (0, 0, 0, min(alpha, 200)))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


# =============================================================================
# SEGMENTAÇÃO PARA RETENÇÃO (4 FRAMES)
# =============================================================================

def split_script_for_retention(
    title: str,
    body_text: str,
) -> Tuple[str, str, str, str]:
    """
    Divide o texto em 4 segmentos para retenção:
    - Hook: parte mais forte (início impactante)
    - Part2: continuação equilibrada
    - Part3: conclusão
    - Reference: só a referência (ex: "Salmo 46:10")
    Retorno: (hook_text, part2_text, part3_text, reference_text).
    """
    lines = [ln.strip() for ln in body_text.strip().split("\n") if ln.strip()]
    if not lines:
        return ("", "", "", title)
    n = len(lines)
    if n <= 3:
        hook = lines[0] if n >= 1 else ""
        part2 = lines[1] if n >= 2 else ""
        part3 = lines[2] if n >= 3 else ""
    else:
        # ~25% hook, ~35% part2, ~35% part3
        i1 = max(1, n // 4)
        i2 = max(i1 + 1, int(n * 0.6))
        hook = "\n".join(lines[:i1])
        part2 = "\n".join(lines[i1:i2])
        part3 = "\n".join(lines[i2:])
    return (hook, part2, part3, title)


# =============================================================================
# SINCRONIZAÇÃO COM VOZ – FORCED ALIGNMENT + SEGMENTAÇÃO POR PAUSAS
# =============================================================================

def get_forced_alignment(audio_path: str, transcript: str) -> Optional[List[Dict[str, Any]]]:
    """
    Obtém timestamps por palavra via ElevenLabs Forced Alignment API.
    Retorna lista de {"text": str, "start": float, "end": float} ou None se falhar.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key or not api_key.strip():
        return None
    if not os.path.isfile(audio_path) or not transcript.strip():
        return None
    logger.info("      → Forced alignment: enviando áudio + texto para ElevenLabs...")
    t0 = time.monotonic()
    try:
        import requests
        url = "https://api.elevenlabs.io/v1/forced-alignment"
        headers = {"xi-api-key": api_key.strip()}
        with open(audio_path, "rb") as f:
            files = {"file": (os.path.basename(audio_path), f, "audio/mpeg")}
            data = {"text": transcript.strip()}
            r = requests.post(url, headers=headers, files=files, data=data, timeout=60)
        if r.status_code != 200:
            logger.warning("      → Forced alignment falhou: %s %s", r.status_code, r.text[:200])
            return None
        out = r.json()
        words = out.get("words") or []
        elapsed = time.monotonic() - t0
        logger.info("      → Forced alignment OK: %d palavras em %.1fs", len(words), elapsed)
        return [{"text": w.get("text", ""), "start": float(w.get("start", 0)), "end": float(w.get("end", 0))} for w in words]
    except Exception as e:
        elapsed = time.monotonic() - t0
        logger.warning("      → Forced alignment não disponível (%.1fs): %s", elapsed, e)
        return None


def _is_break_after(word: str) -> bool:
    """Pausa natural após pontuação forte ou vírgula."""
    w = (word or "").strip()
    if not w:
        return False
    return w.endswith(".") or w.endswith(",") or w.endswith(";") or w.endswith(":") or w.endswith("!") or w.endswith("?") or w.endswith("—")


def segment_into_phrases(
    words: List[Dict[str, Any]],
    min_words: int = PHRASE_MIN_WORDS,
    max_words: int = PHRASE_MAX_WORDS,
    min_duration: float = MIN_SEGMENT_DURATION,
) -> List[Dict[str, Any]]:
    """
    Agrupa palavras em frases de 10–16 palavras em pausas naturais.
    Usa timestamps reais do forced alignment (start/end por palavra).
    Trechos curtos demais são fundidos para tempo mínimo de leitura confortável.
    Retorna lista de {"text": str, "start": float, "end": float}.
    """
    if not words:
        return []
    phrases: List[Dict[str, Any]] = []
    current: List[Dict[str, Any]] = []
    for w in words:
        current.append(w)
        word_count = len(current)
        text = " ".join(c["text"] for c in current).strip()
        at_break = _is_break_after(w["text"])
        if at_break and word_count >= min_words:
            phrases.append({
                "text": text,
                "start": current[0]["start"],
                "end": current[-1]["end"],
            })
            current = []
        elif word_count >= max_words:
            phrases.append({
                "text": text,
                "start": current[0]["start"],
                "end": current[-1]["end"],
            })
            current = []
    if current:
        text = " ".join(c["text"] for c in current).strip()
        phrases.append({
            "text": text,
            "start": current[0]["start"],
            "end": current[-1]["end"],
        })
    # Fusão: trechos com duração < min_duration são unidos ao próximo (ritmo de leitura)
    merged: List[Dict[str, Any]] = []
    for p in phrases:
        dur = p["end"] - p["start"]
        if merged and dur < min_duration and (p["start"] - merged[-1]["end"]) < 0.15:
            merged[-1] = {
                "text": (merged[-1]["text"] + " " + p["text"]).strip(),
                "start": merged[-1]["start"],
                "end": p["end"],
            }
        else:
            merged.append(p)
    return merged


def _fallback_segment_by_pauses(
    body_text: str,
    total_duration: float,
) -> List[Dict[str, Any]]:
    """
    Fallback sem API: divide por pontuação em trechos de 10–16 palavras.
    Atribui duração proporcional ao número de palavras.
    """
    import re
    normalized = " ".join(body_text.strip().split())
    if not normalized:
        return []
    tokens = re.findall(r"[^\s.,;:!?—]+|[.,;:!?—]", normalized)
    words_only = [t for t in tokens if t not in ".,;:!?—"]
    if not words_only:
        return [{"text": normalized, "start": 0.0, "end": max(2.0, total_duration)}]
    n = len(words_only)
    phrase_size = max(PHRASE_MIN_WORDS, min(PHRASE_MAX_WORDS, n // max(1, (int(total_duration) // 2))))
    phrases: List[Dict[str, Any]] = []
    i = 0
    t = 0.0
    step = total_duration / max(1, (n + phrase_size - 1) // phrase_size)
    while i < n:
        take = min(phrase_size, n - i)
        chunk = words_only[i : i + take]
        text = " ".join(chunk)
        start = t
        end = t + step
        t = end
        phrases.append({"text": text, "start": start, "end": end})
        i += take
    if phrases:
        phrases[-1]["end"] = total_duration
    return phrases


# =============================================================================
# TIPOGRAFIA DE MARCA — SEM FONTE GENÉRICA
# Uma família premium (Playfair, Cinzel, Cormorant, DM Serif Display, Montserrat, Poppins, Inter).
# Se a fonte não carregar → RuntimeError explícito (nunca fallback silencioso).
# =============================================================================

def _get_brand_font_manager(fonts_dir: Optional[str] = None):
    """Retorna FontManager. Levanta RuntimeError se não for possível carregar (sem fallback)."""
    base = Path(__file__).resolve().parents[1]
    from core.premium_visuals import FontManager
    path = fonts_dir or str(base / "outputs" / "fonts")
    return FontManager(path)


def _get_phrase_fonts(fonts_dir: Optional[str] = None, is_reference: bool = False) -> ImageFont.FreeTypeFont:
    """Fonte de marca obrigatória. Erro explícito se não carregar."""
    fm = _get_brand_font_manager(fonts_dir)
    if is_reference:
        return fm.get_brand_title_font(int(HEIGHT * 0.038))
    return fm.get_brand_body_font(int(HEIGHT * 0.055))


def _get_header_font(fonts_dir: Optional[str] = None) -> ImageFont.FreeTypeFont:
    """Header: fonte de marca obrigatória. Erro explícito se não carregar."""
    fm = _get_brand_font_manager(fonts_dir)
    return fm.get_brand_title_font(int(HEIGHT * 0.042))


def render_header_band(
    reference: str,
    width: int = WIDTH,
    height_band: int = HEADER_HEIGHT,
    fonts_dir: Optional[str] = None,
) -> Image.Image:
    """
    Faixa fixa do topo: referência bíblica (ex. Gálatas 5:22–23) sobre gradiente escuro.
    Tipografia serif premium, branco quente #F5F2E8, glow + sombra. Contraste máximo.
    """
    if not reference or not reference.strip():
        ref_img = Image.new("RGBA", (width, height_band), (0, 0, 0, 0))
        return ref_img
    band = Image.new("RGBA", (width, height_band), (0, 0, 0, 0))
    draw = ImageDraw.Draw(band)
    # Gradiente escuro: topo mais escuro, transição suave para transparente na base
    for y in range(height_band):
        alpha = int(200 * (1 - 0.65 * y / max(1, height_band)))
        alpha = max(0, min(255, alpha))
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
    draw = ImageDraw.Draw(band)
    font = _get_header_font(fonts_dir)
    text = reference.strip()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    y = (height_band - (bbox[3] - bbox[1])) // 2 - 2
    for dx in (-2, 0, 2):
        for dy in (-2, 0, 2):
            if dx or dy:
                draw.text((x + dx, y + dy), text, font=font, fill=GLOW_RGBA)
    draw.text((x + 2, y + 2), text, font=font, fill=SHADOW_RGBA)
    draw.text((x, y), text, font=font, fill=TEXT_WARM_WHITE)
    return band


def render_phrase_overlay(
    text: str,
    size: Tuple[int, int] = (WIDTH, HEIGHT),
    fonts_dir: Optional[str] = None,
    is_reference: bool = False,
    reference_title: str = "",
) -> Image.Image:
    """
    Um frame: header fixo com referência no topo (se reference_title) + conteúdo centralizado.
    Serif premium, branco quente (#F5F2E8), sombra + glow. Legibilidade perfeita.
    """
    w, h = size
    content_top = HEADER_HEIGHT if reference_title else 0
    content_h = h - content_top
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    padding = int(w * 0.14)
    max_line_width = w - 2 * padding
    font = _get_phrase_fonts(fonts_dir, is_reference=is_reference)
    color = TEXT_WARM_WHITE
    if is_reference:
        color = (240, 235, 220, 250)

    def _wrap(_text: str) -> List[str]:
        words = _text.replace("\n", " ").strip().split()
        if not words:
            return [""]
        out, current = [], []
        for word in words:
            test = " ".join(current + [word])
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_line_width:
                current.append(word)
            else:
                if current:
                    out.append(" ".join(current))
                current = [word]
        if current:
            out.append(" ".join(current))
        return out

    def _draw_centered(_d: ImageDraw.ImageDraw, _t: str, y: int, glow: bool = True):
        bbox = _d.textbbox((0, 0), _t, font=font)
        tw = bbox[2] - bbox[0]
        x = (w - tw) // 2
        if glow and not is_reference:
            for dx in (-2, 0, 2):
                for dy in (-2, 0, 2):
                    if dx or dy:
                        _d.text((x + dx, y + dy), _t, font=font, fill=GLOW_RGBA)
        _d.text((x + 2, y + 2), _t, font=font, fill=SHADOW_RGBA)
        _d.text((x, y), _t, font=font, fill=color)

    lines = _wrap(text)
    line_height = int(h * 0.07) if not is_reference else int(h * 0.05)
    # Centralizar conteúdo na área abaixo do header
    y = content_top + (content_h - line_height * len(lines)) // 2 - line_height // 2
    for line in lines:
        if line:
            _draw_centered(draw, line, y, glow=not is_reference)
        y += line_height

    if reference_title:
        header_band = render_header_band(reference_title, w, HEADER_HEIGHT, fonts_dir)
        overlay.paste(header_band, (0, 0), header_band)
    return overlay


def _wrap_verse_by_width(
    draw: ImageDraw.ImageDraw,
    font: ImageFont.FreeTypeFont,
    text: str,
    max_width: int,
) -> List[str]:
    """Quebra por palavras (nunca cortar palavras/sílabas). Respeita max_width."""
    words = text.replace("\n", " ").strip().split()
    if not words:
        return [""]
    out, current = [], []
    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current.append(word)
        else:
            if current:
                out.append(" ".join(current))
            current = [word]
    if current:
        out.append(" ".join(current))
    return out


def _balance_verse_lines(
    draw: ImageDraw.ImageDraw,
    font: ImageFont.FreeTypeFont,
    lines: List[str],
    max_width: int,
    min_width_ratio: float = VERSE_MIN_LINE_WIDTH_RATIO,
) -> List[str]:
    """
    Evita linha última muito curta (orphan): se a última linha for curta demais,
    tenta colocar todo o conteúdo na linha anterior (se couber). Nunca corta palavras.
    """
    if len(lines) <= 1:
        return lines
    min_width = int(max_width * min_width_ratio)
    last = lines[-1].strip()
    if not last:
        return lines[:-1]
    last_bbox = draw.textbbox((0, 0), last, font=font)
    last_w = last_bbox[2] - last_bbox[0]
    if last_w >= min_width:
        return lines
    prev = lines[-2]
    test_prev = (prev + " " + last).strip()
    bbox = draw.textbbox((0, 0), test_prev, font=font)
    if bbox[2] - bbox[0] <= max_width:
        return lines[:-2] + [test_prev]
    return lines


def _normalize_verse_text_for_render(text: str) -> str:
    """Aplica normalização de exibição antes de renderizar (capitalização, limpeza)."""
    from core.psalm_text_preparation import normalize_text_for_display
    return normalize_text_for_display(text or "").strip()


def render_verse_only_overlay(
    text: str,
    size: Tuple[int, int] = (WIDTH, HEIGHT),
    fonts_dir: Optional[str] = None,
    is_reference: bool = False,
) -> Image.Image:
    """
    Composição tipográfica cinematográfica: centralizada (vertical + horizontal),
    caixa fixa, safe area, quebra só por palavras (nunca cortar letras/sílabas).
    Texto normalizado antes de desenhar. Sem overflow, layout estável.
    """
    w, h = size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = _get_phrase_fonts(fonts_dir, is_reference=is_reference)
    color = TEXT_WARM_WHITE
    if is_reference:
        color = (240, 235, 220, 250)

    # Etapa 1 — Texto limpo para exibição (capitalização, espaços, pontuação)
    text = _normalize_verse_text_for_render(text)
    if not text:
        return overlay

    def _draw_centered_line(_d: ImageDraw.ImageDraw, _t: str, y: int, glow: bool = True) -> None:
        bbox = _d.textbbox((0, 0), _t, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (w - tw) // 2
        # Não desenhar fora da caixa (evita letras cortadas)
        if y + th > VERSE_AREA_BOTTOM or y < VERSE_AREA_TOP:
            return
        if glow and not is_reference:
            for dx in (-2, 0, 2):
                for dy in (-2, 0, 2):
                    if dx or dy:
                        _d.text((x + dx, y + dy), _t, font=font, fill=GLOW_RGBA)
        _d.text((x + 2, y + 2), _t, font=font, fill=SHADOW_RGBA)
        _d.text((x, y), _t, font=font, fill=color)

    # Etapa 2 — Paginação inteligente: quebra só por palavras, densidade equilibrada
    lines = _wrap_verse_by_width(draw, font, text, VERSE_MAX_LINE_WIDTH)
    lines = _balance_verse_lines(draw, font, lines, VERSE_MAX_LINE_WIDTH)
    if not lines:
        return overlay

    line_height = int(VERSE_AREA_HEIGHT * VERSE_LINE_HEIGHT_RATIO) if not is_reference else int(VERSE_AREA_HEIGHT * 0.052)
    total_lines_h = line_height * len(lines)
    if total_lines_h > VERSE_AREA_HEIGHT:
        line_height = max(14, VERSE_AREA_HEIGHT // len(lines))
        total_lines_h = line_height * len(lines)

    # Etapa 3 — Centralização simétrica (vertical + horizontal)
    y_offset = max(0, (VERSE_AREA_HEIGHT - total_lines_h) // 2)
    y = VERSE_AREA_TOP + y_offset
    for line in lines:
        line = line.strip()
        if line:
            _draw_centered_line(draw, line, y, glow=not is_reference)
        y += line_height
    return overlay


# =============================================================================
# RENDER RETENÇÃO – 4 ESTILOS DE FRAME (LEGADO)
# =============================================================================

def _get_retention_fonts(
    frame_index: int,
    fonts_dir: Optional[str] = None,
) -> Tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont]:
    """Fonte de marca obrigatória em todos os frames. Erro explícito se não carregar."""
    fm = _get_brand_font_manager(fonts_dir)
    if frame_index == 3:
        return fm.get_brand_title_font(int(HEIGHT * 0.038)), fm.get_brand_body_font(int(HEIGHT * 0.028))
    if frame_index == 0:
        return fm.get_brand_title_font(int(HEIGHT * 0.072)), fm.get_brand_body_font(int(HEIGHT * 0.058))
    return fm.get_brand_title_font(int(HEIGHT * 0.055)), fm.get_brand_body_font(int(HEIGHT * 0.042))


def render_retention_frame(
    frame_index: int,
    text: str,
    reference: str,
    size: Tuple[int, int] = (WIDTH, HEIGHT),
    fonts_dir: Optional[str] = None,
    golden_light: bool = False,
) -> Image.Image:
    """
    Renderiza um frame da sequência de retenção.
    frame_index: 0=hook (texto MUITO grande), 1=part2, 2=part3 (luz dourada sutil), 3=referência (texto menor).
    """
    w, h = size
    content_top = HEADER_HEIGHT
    content_h = h - content_top
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    padding = int(w * 0.12)
    max_line_width = w - 2 * padding

    title_font, body_font = _get_retention_fonts(frame_index, fonts_dir)
    if frame_index == 3:
        main_font = title_font
        text_to_draw = reference
    else:
        main_font = body_font if len(text) > 60 else title_font
        text_to_draw = text.strip()

    color = TEXT_WARM_WHITE
    if golden_light and frame_index == 2:
        color = (255, 235, 200, 252)

    def _wrap(_text: str, font: ImageFont.FreeTypeFont) -> List[str]:
        words = _text.replace("\n", " ").strip().split()
        if not words:
            return [""]
        out, current = [], []
        for word in words:
            test = " ".join(current + [word])
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_line_width:
                current.append(word)
            else:
                if current:
                    out.append(" ".join(current))
                current = [word]
        if current:
            out.append(" ".join(current))
        return out

    def _draw_centered(d: ImageDraw.ImageDraw, _t: str, font: ImageFont.FreeTypeFont, y: int, fill: tuple, glow: bool = True):
        bbox = d.textbbox((0, 0), _t, font=font)
        tw = bbox[2] - bbox[0]
        x = (w - tw) // 2
        if glow:
            for dx in range(-3, 4, 2):
                for dy in range(-3, 4, 2):
                    d.text((x + dx, y + dy), _t, font=font, fill=GLOW_RGBA)
        d.text((x + 2, y + 2), _t, font=font, fill=SHADOW_RGBA)
        d.text((x, y), _t, font=font, fill=fill)

    lines = _wrap(text_to_draw, main_font)
    if frame_index == 0 and len(lines) > 2:
        lines = lines[:2]
    line_height = int(h * (0.08 if frame_index == 0 else 0.065 if frame_index == 3 else 0.07))
    y = content_top + (content_h - line_height * len(lines)) // 2 - line_height // 2
    for line in lines:
        if line:
            _draw_centered(draw, line, main_font, y, color, glow=(frame_index != 3))
        y += line_height

    if reference:
        header_band = render_header_band(reference, w, HEADER_HEIGHT, fonts_dir)
        overlay.paste(header_band, (0, 0), header_band)
    return overlay


# =============================================================================
# 2. NARRAÇÃO – EXCLUSIVAMENTE EDGE-TTS
# =============================================================================

# Voz obrigatória: pt-BR-ThalitaMultilingualNeural (sem fallback, sem substituição)
EDGE_TTS_VOICE = "pt-BR-ThalitaMultilingualNeural"


def generate_voice(text: str, output_path: str) -> str:
    """
    Gera narração com edge-tts exclusivamente.
    Voz: pt-BR-ThalitaMultilingualNeural. Áudio salvo em MP3.
    Sem fallback: se edge-tts falhar, lança exceção.
    """
    import asyncio
    import edge_tts

    async def _synthesize() -> None:
        communicate = edge_tts.Communicate(text.strip(), EDGE_TTS_VOICE)
        await communicate.save(output_path)

    logger.info("[2/6] Gerando voz (edge-tts – %s)...", EDGE_TTS_VOICE)
    t0 = time.monotonic()
    os.makedirs(os.path.dirname(output_path) or "outputs", exist_ok=True)
    try:
        asyncio.run(_synthesize())
    except Exception as e:
        logger.exception("edge-tts falhou: %s", e)
        err_msg = str(e)
        if "403" in err_msg or "Invalid response status" in err_msg:
            raise RuntimeError(
                "edge-tts retornou 403 (serviço Microsoft recusou a conexão). "
                "Tente: 1) pip install --upgrade edge-tts  2) Se persistir, a Microsoft pode bloquear sua rede/região — teste outra rede ou VPN."
            ) from e
        raise RuntimeError(f"edge-tts falhou: {e}") from e
    size_kb = os.path.getsize(output_path) // 1024
    elapsed = time.monotonic() - t0
    logger.info("[2/6] Narração edge-tts concluída: %s (%d KB) em %.1fs", output_path, size_kb, elapsed)
    return output_path


def _generate_voice_from_segments(
    segments: List[str],
    output_path: str,
) -> Tuple[List[Dict[str, Any]], str]:
    """
    Gera áudio por bloco (cadência preparada), concatena e retorna phrase_segments com tempos exatos.
    Cada bloco = 1 unidade de áudio; tempo de tela = duração real da fala. Sincronização perfeita.
    """
    import tempfile
    from pydub import AudioSegment

    parent = os.path.dirname(output_path)
    if not parent:
        parent = "outputs"
    os.makedirs(parent, exist_ok=True)
    tmp_dir = tempfile.mkdtemp(prefix="salmo_tts_", dir=parent)
    paths: List[str] = []
    used_segments: List[str] = []
    try:
        for i, text in enumerate(segments):
            if not (text or "").strip():
                continue
            p = os.path.join(tmp_dir, f"seg_{i:04d}.mp3")
            generate_voice(text.strip(), p)
            paths.append(p)
            used_segments.append(text.strip())
        if not paths:
            raise RuntimeError("Nenhum segmento de áudio gerado.")
        combined = AudioSegment.empty()
        starts: List[float] = [0.0]
        for p in paths:
            seg = AudioSegment.from_mp3(p)
            combined += seg
            starts.append(starts[-1] + len(seg) / 1000.0)
        combined.export(output_path, format="mp3", bitrate="192k")
        phrase_segments = [
            {"text": used_segments[i], "start": starts[i], "end": starts[i + 1]}
            for i in range(len(used_segments))
        ]
        logger.info("[2/6] Narração por blocos: %d segmentos, %.1fs total", len(phrase_segments), starts[-1])
        return phrase_segments, output_path
    finally:
        for p in paths:
            try:
                if os.path.isfile(p):
                    os.remove(p)
            except OSError:
                pass
        try:
            os.rmdir(tmp_dir)
        except OSError:
            pass


# =============================================================================
# 3. RENDER TEXT OVERLAY
# =============================================================================

def _get_cinematic_fonts(fonts_dir: Optional[str] = None) -> Tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont]:
    """Fonte de marca obrigatória para overlay cinematográfico. Erro explícito se não carregar."""
    fm = _get_brand_font_manager(fonts_dir)
    return fm.get_brand_title_font(int(HEIGHT * 0.048)), fm.get_brand_body_font(int(HEIGHT * 0.032))


def render_text_overlay(
    size: Tuple[int, int] = (WIDTH, HEIGHT),
    title: str = "",
    body_text: str = "",
    fonts_dir: Optional[str] = None,
) -> Image.Image:
    """
    Renderiza overlay de texto centralizado: tipografia elegante (serif),
    sombra suave, layout limpo. Transparência para composição sobre o background.
    """
    w, h = size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    title_font, body_font = _get_cinematic_fonts(fonts_dir)
    padding = int(w * 0.1)
    max_line_width = w - 2 * padding
    text_color = (255, 252, 245, 250)
    shadow_color = (0, 0, 0, 120)

    def _draw_centered(d: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, y: int, color: tuple):
        bbox = d.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (w - tw) // 2
        d.text((x + 2, y + 2), text, font=font, fill=shadow_color)
        d.text((x, y), text, font=font, fill=color)

    def _wrap(text: str, font: ImageFont.FreeTypeFont) -> List[str]:
        lines = []
        for para in text.strip().split("\n"):
            para = para.strip()
            if not para:
                lines.append("")
                continue
            words = para.split()
            current = []
            for word in words:
                test = " ".join(current + [word])
                bbox = draw.textbbox((0, 0), test, font=font)
                if bbox[2] - bbox[0] <= max_line_width:
                    current.append(word)
                else:
                    if current:
                        lines.append(" ".join(current))
                    current = [word]
            if current:
                lines.append(" ".join(current))
        return lines

    y = int(h * 0.12)
    if title:
        _draw_centered(draw, title, title_font, y, text_color)
        y += int(h * 0.08)

    for line in _wrap(body_text, body_font):
        if line:
            _draw_centered(draw, line, body_font, y, text_color)
        y += int(h * 0.045)

    return overlay


# =============================================================================
# 4. COMPOSE VIDEO
# =============================================================================

def compose_video(
    background_image: Image.Image,
    text_overlay: Image.Image,
    voice_audio_path: str,
    output_path: str,
    music_path: Optional[str] = None,
    music_volume: float = 0.18,
    ken_burns_zoom: float = 1.08,
    fade_duration: float = 0.8,
    fps: int = FPS,
) -> str:
    """
    Compõe o vídeo final:
    - Background com Ken Burns (zoom suave) + color grading + glow
    - Overlay de texto com fade-in e fade-out
    - Áudio: voz + música ambiente (se music_path) com mixagem profissional
    - Saída 1080x1920, duração = duração do áudio de voz
    """
    from moviepy.editor import (
        ImageClip,
        AudioFileClip,
        CompositeVideoClip,
        CompositeAudioClip,
    )
    from moviepy.video.fx.all import fadein, fadeout

    voice_clip = AudioFileClip(voice_audio_path)
    duration = voice_clip.duration

    if duration < 1.0:
        duration = 1.0

    # Background: color grading + glow
    bg_np = np.array(_apply_soft_glow(_apply_spiritual_grading(background_image.copy())))
    bg_clip = ImageClip(bg_np, duration=duration)

    # Ken Burns: zoom suave ao longo do tempo (resize progressivo)
    try:
        def zoom_factor(t):
            return 1.0 + (ken_burns_zoom - 1.0) * min(1.0, t / duration)
        bg_clip = bg_clip.resize(zoom_factor).set_position("center")
    except Exception as _e:
        logger.debug("Ken Burns fallback para estático: %s", _e)
        bg_clip = bg_clip.set_position("center")

    # Overlay de texto com fade in/out
    overlay_np = np.array(text_overlay)
    overlay_clip = ImageClip(overlay_np, duration=duration).set_position((0, 0))
    overlay_clip = overlay_clip.fx(fadein, fade_duration).fx(fadeout, fade_duration)

    composite = CompositeVideoClip([bg_clip, overlay_clip], size=(WIDTH, HEIGHT))

    # Áudio: música ambiente abaixo da voz (crossfade suave, mixagem profissional)
    if music_path and os.path.isfile(music_path):
        try:
            from pydub import AudioSegment
            music = AudioSegment.from_file(music_path)
            music = music - 18  # dB abaixo
            music = music[: int(duration * 1000)]
            music_path_trimmed = voice_audio_path.replace(".mp3", "_music_trim.mp3")
            music.export(music_path_trimmed, format="mp3")
            music_clip = AudioFileClip(music_path_trimmed)
            music_clip = music_clip.volumex(music_volume)
            voice_only = voice_clip.volumex(1.0)
            final_audio = CompositeAudioClip([music_clip, voice_only])
            composite = composite.set_audio(final_audio)
            music_clip.close()
            if os.path.exists(music_path_trimmed):
                os.remove(music_path_trimmed)
        except Exception as e:
            logger.warning("Música ambiente ignorada: %s", e)
            composite = composite.set_audio(voice_clip)
    else:
        composite = composite.set_audio(voice_clip)

    os.makedirs(os.path.dirname(output_path) or "outputs", exist_ok=True)
    composite.write_videofile(
        output_path,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        bitrate="12000k",
        audio_bitrate="192k",
        preset="medium",
        threads=4,
        logger=None,
    )

    voice_clip.close()
    bg_clip.close()
    overlay_clip.close()
    composite.close()

    logger.info("Vídeo cinematográfico exportado: %s (%.1fs)", output_path, duration)
    return output_path


def compose_retention_video(
    background_image: Image.Image,
    overlay_images: Sequence[Image.Image],
    voice_audio_path: str,
    segment_texts: Tuple[str, str, str, str],
    output_path: str,
    music_path: Optional[str] = None,
    music_volume: float = 0.18,
    fps: int = FPS,
) -> str:
    """
    Compõe o vídeo de retenção em 4 segmentos:
    - Fundo dark cinematic + movimento (zoom/drift) em todos os frames
    - Hook: fade-in rápido (0.35s); Referência: fade-out cinematográfico
    - Durações: 3 segmentos narrados proporcional ao texto + 2.5s referência
    """
    from moviepy.editor import (
        ImageClip,
        AudioFileClip,
        CompositeVideoClip,
        CompositeAudioClip,
        concatenate_videoclips,
        concatenate_audioclips,
    )
    from moviepy.video.fx.all import fadein, fadeout
    from moviepy.audio.AudioClip import AudioClip

    assert len(overlay_images) >= 4 and len(segment_texts) >= 4
    logger.info("[4/6] Compondo vídeo retenção (4 frames)...")
    t_retention = time.monotonic()
    voice_clip = AudioFileClip(voice_audio_path)
    total_voice = voice_clip.duration
    if total_voice < 1.0:
        total_voice = 1.0
    hook_t, part2_t, part3_t, ref_t = segment_texts[0], segment_texts[1], segment_texts[2], segment_texts[3]
    total_chars = max(1, len(hook_t) + len(part2_t) + len(part3_t))
    d1 = total_voice * len(hook_t) / total_chars
    d2 = total_voice * len(part2_t) / total_chars
    d3 = total_voice - d1 - d2
    if d3 < 0.5:
        d3 = 0.5
        d1 = min(d1, total_voice - d2 - d3)
        d2 = total_voice - d1 - d3
    d4 = REFERENCE_FRAME_DURATION
    durations = [d1, d2, d3, d4]

    def _make_bg_np(img: Image.Image, golden: bool = False) -> np.ndarray:
        b = _apply_dark_cinematic_grading(img.copy(), vignette_strength=0.5)
        b = _apply_soft_glow(b, radius=20, strength=0.08)
        if golden:
            r, g, bl = b.split()
            r = r.point(lambda x: min(255, int(x * 1.08)))
            bl = bl.point(lambda x: max(0, int(x * 0.92)))
            b = Image.merge("RGB", (r, g, bl))
        return np.array(b)

    # Zoom contínuo nos 4 segmentos: 1.0 → 1.015 → 1.03 → 1.045 → 1.06 (uma tomada)
    zoom_per_seg = 0.06 / 4
    crossfade_ret = 0.6

    clips = []
    for i in range(4):
        dur = durations[i]
        golden = i == 2
        z_start = 1.0 + zoom_per_seg * i
        z_end = 1.0 + zoom_per_seg * (i + 1)
        bg_np = _make_bg_np(background_image, golden=golden)
        bg_clip = ImageClip(bg_np, duration=dur)
        try:
            (zs, ze, d) = (z_start, z_end, dur)
            bg_clip = bg_clip.resize(
                lambda t, z_start=zs, z_end=ze, seg_dur=d: z_start + (z_end - z_start) * min(1.0, t / max(0.01, seg_dur))
            ).set_position("center")
        except Exception:
            bg_clip = bg_clip.set_position("center")
        ov_np = np.array(overlay_images[i])
        overlay_clip = ImageClip(ov_np, duration=dur).set_position((0, 0))
        if i == 0:
            overlay_clip = overlay_clip.fx(fadein, min(0.5, dur * 0.2))
        else:
            overlay_clip = overlay_clip.fx(fadein, min(crossfade_ret, dur * 0.3))
        overlay_clip = overlay_clip.fx(fadeout, min(crossfade_ret, dur * 0.35) if i < 3 else min(1.2, dur * 0.5))
        comp = CompositeVideoClip([bg_clip, overlay_clip], size=(WIDTH, HEIGHT))
        clips.append(comp)

    final = concatenate_videoclips(clips)
    total_duration = final.duration
    # Áudio: voz nos primeiros d1+d2+d3, silêncio no último segmento
    voice_trimmed = voice_clip.subclip(0, d1 + d2 + d3)
    # Silêncio no segmento de referência (d4 segundos)
    try:
        silence = AudioClip(lambda t: np.zeros(1), duration=d4, fps=44100)
        voice_with_silence = concatenate_audioclips([voice_trimmed, silence])
    except Exception:
        voice_with_silence = voice_trimmed

    if music_path and os.path.isfile(music_path):
        try:
            from pydub import AudioSegment
            music = AudioSegment.from_file(music_path)
            music = music - 18
            music = music[: int(total_duration * 1000)]
            music_path_trimmed = voice_audio_path.replace(".mp3", "_music_retention.mp3")
            music.export(music_path_trimmed, format="mp3")
            music_clip = AudioFileClip(music_path_trimmed)
            music_clip = music_clip.volumex(music_volume).set_duration(total_duration)
            voice_only = voice_with_silence.volumex(1.0)
            if voice_only.duration > total_duration:
                voice_only = voice_only.subclip(0, total_duration)
            final_audio = CompositeAudioClip([music_clip, voice_only])
            final = final.set_audio(final_audio)
            music_clip.close()
            if os.path.exists(music_path_trimmed):
                os.remove(music_path_trimmed)
        except Exception as e:
            logger.warning("Música retenção ignorada: %s", e)
            final = final.set_audio(voice_with_silence)
    else:
        final = final.set_audio(voice_with_silence)

    os.makedirs(os.path.dirname(output_path) or "outputs", exist_ok=True)
    logger.info("[5/6] Exportando MP4 (pode levar 2–5 min; aguarde)...")
    t_export_ret = time.monotonic()
    final.write_videofile(
        output_path,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        bitrate="12000k",
        audio_bitrate="192k",
        preset="medium",
        threads=4,
        logger=None,
    )
    export_ret_elapsed = time.monotonic() - t_export_ret
    voice_clip.close()
    for c in clips:
        c.close()
    final.close()
    logger.info("[5/6] Vídeo retenção exportado em %.1fs: %s (%.1fs)", export_ret_elapsed, output_path, total_duration)
    return output_path


def _rgba_to_rgb_and_mask(arr: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Converte (H,W,4) RGBA para RGB e máscara (0–1) para MoviePy."""
    rgb = arr[..., :3].copy()
    mask = (arr[..., 3] / 255.0).astype(np.float32)
    return rgb, mask


def compose_synced_video(
    background_image: Image.Image,
    phrase_segments: List[Dict[str, Any]],
    reference_title: str,
    voice_audio_path: str,
    output_path: str,
    music_path: Optional[str] = None,
    music_volume: float = 0.18,
    fps: int = FPS,
    crossfade: float = CROSSFADE_DURATION,
) -> str:
    """
    Compõe vídeo com arquitetura de 3 camadas fixas.
    Camada 1: um único fundo (renderizado uma vez, zoom contínuo 1.0→1.06).
    Camada 2: um único header (referência bíblica, nunca re-renderizado).
    Camada 3: overlays só do verso, com crossfade suave entre segmentos.
    """
    from moviepy.editor import (
        ImageClip,
        AudioFileClip,
        CompositeVideoClip,
        CompositeAudioClip,
        concatenate_audioclips,
    )
    from moviepy.video.fx.all import fadein, fadeout
    from moviepy.audio.AudioClip import AudioClip

    logger.info("[4/6] Compondo vídeo sincronizado (3 camadas): %d frases + referência", len(phrase_segments))
    t_compose = time.monotonic()
    voice_clip = AudioFileClip(voice_audio_path)
    durs = [max(0.5, s["end"] - s["start"]) for s in phrase_segments]
    narration_end = sum(durs)
    if narration_end < 0.5:
        narration_end = voice_clip.duration
        durs = [narration_end] if phrase_segments else []
    ref_dur = REFERENCE_FRAME_DURATION_SYNC
    total_duration = narration_end + ref_dur

    def _make_bg_np(img: Image.Image, golden: bool = False) -> np.ndarray:
        b = _apply_dark_cinematic_grading(img.copy(), vignette_strength=0.5)
        b = _apply_soft_glow(b, radius=20, strength=0.08)
        if golden:
            r, g, bl = b.split()
            r = r.point(lambda x: min(255, int(x * 1.05)))
            bl = bl.point(lambda x: max(0, int(x * 0.95)))
            b = Image.merge("RGB", (r, g, bl))
        return np.array(b)

    # —— Camada 1: um único fundo, zoom contínuo do início ao fim ——
    bg_np = _make_bg_np(background_image, golden=True)
    bg_clip = ImageClip(bg_np, duration=total_duration)
    try:
        tot = total_duration
        bg_clip = bg_clip.resize(
            lambda t, _tot=tot: 1.0 + 0.06 * min(1.0, t / max(0.01, _tot))
        ).set_position("center")
    except Exception:
        bg_clip = bg_clip.set_position("center")

    # —— Camada 2: um único header (referência no topo), nunca re-renderizado ——
    header_band = render_header_band(reference_title, WIDTH, HEADER_HEIGHT)
    header_full = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    header_full.paste(header_band, (0, 0), header_band)
    header_rgba = np.array(header_full)
    header_rgb, header_mask = _rgba_to_rgb_and_mask(header_rgba)
    header_clip = ImageClip(header_rgb, duration=total_duration).set_position((0, 0))
    mask_clip = ImageClip(header_mask, ismask=True).set_duration(total_duration)
    header_clip = header_clip.set_mask(mask_clip)

    # —— Camada 3: overlays só do verso; troca no exato momento da pronúncia ——
    verse_clips = []
    for i, seg in enumerate(phrase_segments):
        dur = durs[i]
        start = sum(durs[:i])  # início exato do segmento (timestamps da voz)
        overlay = render_verse_only_overlay(seg["text"])
        rgba = np.array(overlay)
        rgb, mask = _rgba_to_rgb_and_mask(rgba)
        clip = ImageClip(rgb, duration=dur).set_position((0, 0)).set_mask(
            ImageClip(mask, ismask=True).set_duration(dur)
        )
        clip = clip.set_start(start)
        if i == 0:
            clip = clip.fx(fadein, min(0.4, dur * 0.2))
        else:
            clip = clip.fx(fadein, min(0.35, dur * 0.2))
        clip = clip.fx(fadeout, min(crossfade, dur * 0.3))
        verse_clips.append(clip)

    # Referência: começa no fim da narração, crossfade com último verso
    start_ref = narration_end - crossfade
    ref_overlay = render_verse_only_overlay(reference_title, is_reference=True)
    ref_rgba = np.array(ref_overlay)
    ref_rgb, ref_mask = _rgba_to_rgb_and_mask(ref_rgba)
    ref_dur_ext = ref_dur + crossfade
    ref_clip = ImageClip(ref_rgb, duration=ref_dur_ext).set_position((0, 0)).set_mask(
        ImageClip(ref_mask, ismask=True).set_duration(ref_dur_ext)
    )
    ref_clip = ref_clip.set_start(start_ref)
    ref_clip = ref_clip.fx(fadein, min(crossfade, ref_dur * 0.25)).fx(fadeout, min(0.8, ref_dur * 0.4))
    verse_clips.append(ref_clip)
    logger.info("      → Camada 1: fundo único | Camada 2: header único | Camada 3: %d overlays verso", len(verse_clips))

    final = CompositeVideoClip([bg_clip, header_clip] + verse_clips, size=(WIDTH, HEIGHT))
    final = final.set_duration(total_duration)

    voice_trimmed = voice_clip.subclip(0, min(narration_end, voice_clip.duration))
    try:
        silence = AudioClip(lambda t: np.zeros(1), duration=ref_dur, fps=44100)
        voice_with_silence = concatenate_audioclips([voice_trimmed, silence])
    except Exception:
        voice_with_silence = voice_trimmed

    if music_path and os.path.isfile(music_path):
        try:
            from pydub import AudioSegment
            music = AudioSegment.from_file(music_path)
            music = music - 18
            music = music[: int(total_duration * 1000)]
            music_path_trimmed = voice_audio_path.replace(".mp3", "_music_sync.mp3")
            music.export(music_path_trimmed, format="mp3")
            music_clip = AudioFileClip(music_path_trimmed)
            music_clip = music_clip.volumex(music_volume).set_duration(total_duration)
            voice_only = voice_with_silence.volumex(1.0)
            if voice_only.duration > total_duration:
                voice_only = voice_only.subclip(0, total_duration)
            final_audio = CompositeAudioClip([music_clip, voice_only])
            final = final.set_audio(final_audio)
            music_clip.close()
            if os.path.exists(music_path_trimmed):
                os.remove(music_path_trimmed)
        except Exception as e:
            logger.warning("Música sync ignorada: %s", e)
            final = final.set_audio(voice_with_silence)
    else:
        final = final.set_audio(voice_with_silence)

    os.makedirs(os.path.dirname(output_path) or "outputs", exist_ok=True)
    logger.info("[5/6] Exportando MP4 (pode levar 2–5 min; aguarde)...")
    t_export = time.monotonic()
    try:
        final.write_videofile(
            output_path,
            fps=fps,
            codec="libx264",
            audio_codec="aac",
            bitrate="12000k",
            audio_bitrate="192k",
            preset="medium",
            threads=4,
            logger=None,
        )
    except Exception as e:
        logger.error("Erro ao exportar vídeo: %s", e)
        raise
    export_elapsed = time.monotonic() - t_export
    voice_clip.close()
    bg_clip.close()
    header_clip.close()
    for c in verse_clips:
        c.close()
    final.close()
    total_elapsed = time.monotonic() - t_compose
    logger.info("[5/6] Vídeo exportado em %.1fs (encoding: %.1fs): %s (%.1fs, %d frases)", total_elapsed, export_elapsed, output_path, total_duration, len(phrase_segments))
    return output_path


# =============================================================================
# PIPELINE UNIFICADO
# =============================================================================

def _find_ambient_music(assets_dir: Optional[str] = None) -> Optional[str]:
    """Procura música ambiente em assets/ (ambient*.mp3, music/*.mp3, etc.)."""
    base = Path(__file__).resolve().parents[1]
    path = (base / (assets_dir or ASSETS_DIR_DEFAULT)) if assets_dir else (base / ASSETS_DIR_DEFAULT)
    if not path.exists():
        return None
    for pattern in ("ambient*.mp3", "music/*.mp3", "*.mp3"):
        for f in sorted(path.glob(pattern)):
            if f.is_file():
                return str(f)
    return None


def run_cinematic_salmo_pipeline(
    title: str,
    body_text: str,
    output_dir: str = "outputs",
    assets_dir: Optional[str] = None,
    music_path: Optional[str] = None,
    output_filename: Optional[str] = None,
) -> dict:
    """
    Pipeline cinematográfico sincronizado: texto acompanha a voz.
    - Preparação textual: normalização, cadência (pausas por pontuação), equilíbrio visual.
    - Se vários blocos: TTS por bloco + merge → sincronização exata. Senão: TTS único + Forced Alignment ou fallback.
    - Cada frame = duração real da fala; crossfade suave; tipografia premium.
    """
    from datetime import datetime

    t_pipeline_start = time.monotonic()
    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    logger.info("Pipeline Salmo do Dia (sincronizado) – Iniciando")
    bg = load_background(assets_dir)

    # Etapa 0 — Preparação textual: cadência, pausas naturais, equilíbrio visual
    from core.psalm_text_preparation import prepare_psalm_for_narration
    prepared = prepare_psalm_for_narration(body_text)
    segments_prep = prepared.get("segments") or []
    text_for_tts = prepared.get("normalized") or body_text

    voice_path = os.path.join(output_dir, f"voice_salmo_{ts}.mp3")
    phrase_segments: List[Dict[str, Any]] = []

    if len(segments_prep) >= 2:
        # Narração por blocos: cada bloco = 1 áudio, merge, tempos exatos (ritmo + sincronização perfeita)
        logger.info("[2/6] Gerando voz por blocos (cadência preparada)...")
        phrase_segments, voice_path = _generate_voice_from_segments(segments_prep, voice_path)
    else:
        # Um único bloco ou preparação não quebrou: TTS único + forced alignment ou fallback
        generate_voice(text_for_tts, voice_path)
        logger.info("[3/6] Obtendo duração do áudio e segmentando texto...")
        voice_duration = 0.0
        try:
            from moviepy.editor import AudioFileClip
            ac = AudioFileClip(voice_path)
            voice_duration = ac.duration
            ac.close()
        except Exception:
            pass
        if voice_duration < 1.0:
            voice_duration = 25.0
        words = get_forced_alignment(voice_path, text_for_tts)
        if words:
            phrase_segments = segment_into_phrases(words, min_words=PHRASE_MIN_WORDS, max_words=PHRASE_MAX_WORDS)
            logger.info("[3/6] Sincronização por Forced Alignment: %d frases", len(phrase_segments))
        if not phrase_segments:
            phrase_segments = _fallback_segment_by_pauses(text_for_tts, voice_duration)
            logger.info("[3/6] Fallback por pontuação: %d frases, duração proporcional", len(phrase_segments))

    if not phrase_segments:
        logger.info("[3/6] Usando fluxo de retenção (4 frames fixos)")
        hook_text, part2_text, part3_text, reference_text = split_script_for_retention(title, body_text)
        segment_texts = (hook_text, part2_text, part3_text, reference_text)
        overlay_images = [
            render_retention_frame(0, hook_text, reference_text, (WIDTH, HEIGHT), None, False),
            render_retention_frame(1, part2_text, reference_text, (WIDTH, HEIGHT), None, False),
            render_retention_frame(2, part3_text, reference_text, (WIDTH, HEIGHT), None, True),
            render_retention_frame(3, "", reference_text, (WIDTH, HEIGHT), None, False),
        ]
        music = music_path or _find_ambient_music(assets_dir)
        out_name = output_filename or f"salmo_cinematic_{ts}.mp4"
        video_path = os.path.join(output_dir, out_name)
        compose_retention_video(
            background_image=bg,
            overlay_images=overlay_images,
            voice_audio_path=voice_path,
            segment_texts=segment_texts,
            output_path=video_path,
            music_path=music,
        )
    else:
        music = music_path or _find_ambient_music(assets_dir)
        if music:
            logger.info("      Música ambiente: %s", music)
        out_name = output_filename or f"salmo_cinematic_{ts}.mp4"
        video_path = os.path.join(output_dir, out_name)
        compose_synced_video(
            background_image=bg,
            phrase_segments=phrase_segments,
            reference_title=title,
            voice_audio_path=voice_path,
            output_path=video_path,
            music_path=music,
        )

    total_elapsed = time.monotonic() - t_pipeline_start
    logger.info("[6/6] Pipeline concluído com sucesso em %.1fs total", total_elapsed)
    return {
        "video_path": video_path,
        "audio_path": voice_path,
        "duration_seconds": None,
    }
