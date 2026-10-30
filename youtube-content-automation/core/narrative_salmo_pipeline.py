"""
Pipeline de filme narrativo cinematográfico baseado em Salmo.

Fluxo:
  SALMO → ANÁLISE → ROTEIRO/STORYBOARD → CENAS (Leonardo)
  → NARRAÇÃO (edge-tts) → TRILHA/SFX → EDIÇÃO (MoviePy) → MP4

Duração alvo: ≥ 120 segundos (preferencialmente 140–165s).
"""

from __future__ import annotations

import json
import logging
import math
import os
import subprocess
import time
import wave
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

WIDTH, HEIGHT = 1920, 1080
FPS = 24
CROSSFADE = 0.35
VOICE_START = 0.05  # voz quase no início da cena (evita pausa longa)
SCENE_TAIL = 0.25   # folga após a fala
EDGE_TTS_VOICE = "pt-BR-FranciscaNeural"  # PT-BR puro (evita Multilingual misturar idiomas)
EDGE_TTS_DIALOGUE = "pt-BR-AntonioNeural"


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def write_docs(out_dir: Path, analysis: Dict[str, Any], characters: List[Dict], scenes: List[Dict], narration: str) -> None:
    docs = out_dir / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "01_analise.md").write_text(
        "# Análise — Salmo 23\n\n"
        + "\n".join(f"**{k.replace('_', ' ').title()}:** {v}\n" for k, v in analysis.items() if k != "simbolos")
        + "\n## Símbolos\n"
        + "\n".join(f"- **{k}:** {v}" for k, v in analysis.get("simbolos", {}).items()),
        encoding="utf-8",
    )
    char_md = ["# Personagens\n"]
    for c in characters:
        char_md.append(f"## {c['nome']}\n")
        for k, v in c.items():
            if k != "nome":
                char_md.append(f"- **{k}:** {v}")
        char_md.append("")
    (docs / "02_personagens.md").write_text("\n".join(char_md), encoding="utf-8")
    sb = ["# Storyboard\n"]
    for s in scenes:
        sb.append(f"## Cena {s['num']} — {s['act'].upper()} ({s['duration']}s)\n")
        sb.append(f"- **Cenário:** {s['cenario']}")
        sb.append(f"- **Personagens:** {', '.join(s['personagens'])}")
        sb.append(f"- **Ação:** {s['acao']}")
        sb.append(f"- **Emoção:** {s['emocao']}")
        sb.append(f"- **Diálogo:** {s.get('dialogo') or '—'}")
        sb.append(f"- **Narração:** {s['narracao']}")
        sb.append(f"- **Câmera:** {s['camera']}")
        sb.append(f"- **Iluminação:** {s['iluminacao']}")
        sb.append(f"- **SFX:** {', '.join(s.get('sfx') or [])}")
        sb.append(f"- **Texto na tela:** {s.get('texto_tela') or '—'}")
        sb.append(f"- **Transição:** {s['transicao']}")
        sb.append(f"- **Prompt:** `{s['prompt'][:220]}...`\n")
    (docs / "03_storyboard.md").write_text("\n".join(sb), encoding="utf-8")
    (docs / "04_narracao.md").write_text(
        "# Narração\n\nVoz: `pt-BR-ThalitaMultilingualNeural`\n\n" + narration,
        encoding="utf-8",
    )
    (docs / "05_audio.md").write_text(
        "# Estratégia de áudio\n\n"
        "- Abertura: pad suave\n"
        "- Desenvolvimento pastoral: cordas leves\n"
        "- Conflito: drones escuros\n"
        "- Clímax: crescendo\n"
        "- Conclusão: resolução em paz\n"
        "- SFX: vento, passos, ovelhas, água, trovões, respiração, harmonia\n",
        encoding="utf-8",
    )


def _sanitize_pt_text(text: str) -> str:
    """Normaliza texto para TTS em português brasileiro (sem símbolos que confundem a voz)."""
    t = (text or "").strip()
    for a, b in [
        ("…", ","),
        ("...", ","),
        ("—", ","),
        ("–", ","),
        ("“", '"'),
        ("”", '"'),
        ("‘", "'"),
        ("’", "'"),
    ]:
        t = t.replace(a, b)
    # remove travessões de diálogo estilo roteiro
    if t.startswith(", "):
        t = t[2:]
    t = " ".join(t.split())
    t = t.replace(" ,", ",").replace(" .", ".").replace(" ?", "?").replace(" !", "!")
    return t


def generate_voice(text: str, output_path: str, voice: str = EDGE_TTS_VOICE, rate: str = "-3%") -> str:
    """Gera TTS em PT-BR e remove o chiado/click típico do início do edge-tts."""
    import edge_tts
    import asyncio

    text = _sanitize_pt_text(text)
    raw_mp3 = str(Path(output_path).with_suffix("")) + "_raw.mp3"
    out_wav = str(Path(output_path).with_suffix(".wav"))

    async def _run():
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(raw_mp3)

    asyncio.run(_run())

    raw_dur = _ffprobe_duration(raw_mp3) or 2.0
    trim_start = 0.045 if raw_dur > 0.5 else 0.015
    kept = max(0.2, raw_dur - trim_start)
    fade_out_st = max(0.05, kept - 0.07)

    af = (
        f"atrim=start={trim_start:.3f},asetpts=PTS-STARTPTS,"
        "afade=t=in:st=0:d=0.025,"
        f"afade=t=out:st={fade_out_st:.3f}:d=0.06,"
        "highpass=f=90,"
        "lowpass=f=7800,"
        "loudnorm=I=-16:TP=-1.5:LRA=9"
    )
    subprocess.check_call(
        ["ffmpeg", "-y", "-i", raw_mp3, "-ac", "1", "-ar", "44100", "-af", af, out_wav],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    final_dur = _ffprobe_duration(out_wav)
    if final_dur < max(0.5, raw_dur * 0.5):
        # Fallback seguro: só fade, sem trim
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-i", raw_mp3,
                "-ac", "1", "-ar", "44100",
                "-af", "afade=t=in:d=0.03,afade=t=out:st=0:d=0.05,loudnorm=I=-16:TP=-1.5:LRA=9",
                out_wav,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    try:
        os.remove(raw_mp3)
    except OSError:
        pass

    if output_path.endswith(".mp3"):
        subprocess.check_call(
            ["ffmpeg", "-y", "-i", out_wav, "-codec:a", "libmp3lame", "-b:a", "192k", output_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return output_path
    return out_wav


def generate_scene_voices(scenes: List[Dict], audio_dir: Path, force: bool = True) -> List[Dict[str, Any]]:
    audio_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for s in scenes:
        path = audio_dir / f"narration_{s['num']:02d}.wav"
        if force and path.exists():
            try:
                path.unlink()
            except OSError:
                pass
        if force or not path.exists() or path.stat().st_size < 1000:
            logger.info("[TTS PT-BR] Cena %d", s["num"])
            generate_voice(s["narracao"], str(path), EDGE_TTS_VOICE, rate="-3%")
            if s.get("dialogo"):
                dpath = audio_dir / f"dialogue_{s['num']:02d}.wav"
                generate_voice(s["dialogo"], str(dpath), EDGE_TTS_DIALOGUE, rate="-6%")
        dur = _ffprobe_duration(str(path))
        results.append({"scene": s["num"], "path": str(path), "duration": max(dur, 0.8), "text": s["narracao"]})
    return results


def _ffprobe_duration(path: str) -> float:
    try:
        out = subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                path,
            ],
            text=True,
        ).strip()
        return float(out)
    except Exception:
        return 0.0


def _write_wav(path: Path, samples: np.ndarray, sr: int = 44100) -> str:
    samples = np.clip(samples, -1.0, 1.0)
    pcm = (samples * 32767.0).astype(np.int16)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())
    return str(path)


def synthesize_score(duration: float, out_path: Path, sr: int = 44100) -> str:
    """Trilha original procedural: pad emocional com arco abertura→tensão→clímax→paz."""
    n = int(duration * sr)
    t = np.linspace(0, duration, n, endpoint=False)

    def env(start, rise, hold, fall):
        e = np.zeros_like(t)
        for i, ti in enumerate(t):
            if ti < start:
                e[i] = 0
            elif ti < start + rise:
                e[i] = (ti - start) / max(rise, 1e-6)
            elif ti < start + rise + hold:
                e[i] = 1.0
            elif ti < start + rise + hold + fall:
                e[i] = 1.0 - (ti - start - rise - hold) / max(fall, 1e-6)
            else:
                e[i] = 0
        return np.clip(e, 0, 1)

    # Harmonic pads
    freqs_open = [110.0, 164.8, 220.0, 329.6]  # Am-ish warmth
    freqs_tense = [98.0, 146.8, 196.0, 233.1]
    freqs_climax = [130.8, 196.0, 261.6, 392.0]
    freqs_peace = [130.8, 164.8, 196.0, 261.6, 329.6]

    sig = np.zeros(n)
    phases = {
        "open": (0, duration * 0.28),
        "tense": (duration * 0.25, duration * 0.55),
        "climax": (duration * 0.50, duration * 0.72),
        "peace": (duration * 0.68, duration),
    }

    def add_chord(freqs, t0, t1, amp=0.045):
        mask = (t >= t0) & (t <= t1)
        local = np.zeros(n)
        fade = env(t0, 2.5, max(0.1, (t1 - t0) - 5.0), 3.0)
        for i, f in enumerate(freqs):
            local += np.sin(2 * math.pi * f * t + i * 0.3) * (amp / (1 + 0.15 * i))
            local += 0.35 * np.sin(2 * math.pi * (f * 2) * t) * (amp / (2 + i))
        sig[:] += local * fade

    add_chord(freqs_open, *phases["open"], amp=0.05)
    add_chord(freqs_tense, *phases["tense"], amp=0.055)
    add_chord(freqs_climax, *phases["climax"], amp=0.07)
    add_chord(freqs_peace, *phases["peace"], amp=0.06)

    # Soft shimmer (sem ruído branco — evita chiado)
    shimmer = 0.005 * np.sin(2 * math.pi * 0.05 * t) * np.sin(2 * math.pi * 660 * t)
    sig += shimmer * env(0, 5, duration - 10, 5)

    # Master envelope (sem noise bed)
    master = env(0, 1.5, duration - 4.5, 3.0)
    sig *= master
    peak = np.max(np.abs(sig)) + 1e-9
    sig = sig / peak * 0.40
    return _write_wav(out_path, sig, sr)


def synthesize_sfx_bank(sfx_dir: Path, sr: int = 44100) -> Dict[str, str]:
    sfx_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(91)
    bank = {}

    def noise_whoosh(seconds, amp=0.2, cutoff=400):
        n = int(seconds * sr)
        x = rng.normal(0, 1, n)
        k = max(3, int(sr / cutoff))
        x = np.convolve(x, np.ones(k) / k, mode="same")
        fade = np.linspace(0, 1, n)
        fade = np.minimum(fade, fade[::-1]) ** 0.7
        return x * fade * amp

    bank["vento_leve"] = _write_wav(sfx_dir / "vento_leve.wav", noise_whoosh(4.0, 0.12, 300))
    bank["vento_forte"] = _write_wav(sfx_dir / "vento_forte.wav", noise_whoosh(3.5, 0.25, 180))
    bank["vento_grama"] = _write_wav(sfx_dir / "vento_grama.wav", noise_whoosh(3.0, 0.1, 500))

    # footsteps
    n = int(2.5 * sr)
    steps = np.zeros(n)
    for center in [0.3, 0.9, 1.5, 2.1]:
        i = int(center * sr)
        length = int(0.08 * sr)
        burst = rng.normal(0, 1, length) * np.hanning(length) * 0.5
        steps[i : i + length] += burst
    bank["passos"] = _write_wav(sfx_dir / "passos.wav", steps)

    # water
    n = int(3 * sr)
    water = np.zeros(n)
    for _ in range(40):
        i = rng.integers(0, n - 2000)
        length = rng.integers(800, 2000)
        tone = np.sin(2 * math.pi * rng.uniform(400, 900) * np.arange(length) / sr)
        water[i : i + length] += tone * np.hanning(length) * 0.08
    bank["agua"] = _write_wav(sfx_dir / "agua.wav", water)

    # sheep-ish bleat (simple formant-ish)
    n = int(1.2 * sr)
    t = np.arange(n) / sr
    bleat = np.sin(2 * math.pi * 280 * t) * np.sin(2 * math.pi * 18 * t)
    bleat += 0.3 * np.sin(2 * math.pi * 560 * t)
    bleat *= np.hanning(n) * 0.25
    bank["ovelhas"] = _write_wav(sfx_dir / "ovelhas.wav", bleat)
    bank["ovelhas_inquietas"] = bank["ovelhas"]

    # thunder distant
    n = int(2.5 * sr)
    th = rng.normal(0, 1, n)
    th = np.convolve(th, np.ones(800) / 800, mode="same")
    th *= np.hanning(n) * 0.35
    bank["trovao_distante"] = _write_wav(sfx_dir / "trovao.wav", th)

    # breath
    n = int(1.5 * sr)
    br = rng.normal(0, 1, n)
    br = np.convolve(br, np.ones(120) / 120, mode="same") * np.hanning(n) * 0.08
    bank["respiracao"] = _write_wav(sfx_dir / "respiracao.wav", br)

    # birds chirp
    n = int(2 * sr)
    birds = np.zeros(n)
    for start in [0.2, 0.7, 1.3]:
        i0 = int(start * sr)
        length = int(0.15 * sr)
        tt = np.arange(length) / sr
        chirp = np.sin(2 * math.pi * (1800 + 600 * tt / 0.15) * tt) * np.hanning(length) * 0.12
        birds[i0 : i0 + length] += chirp
    bank["passaros"] = _write_wav(sfx_dir / "passaros.wav", birds)
    bank["passaros_noite"] = bank["passaros"]
    bank["folhas"] = bank["vento_grama"]
    bank["eco"] = bank["vento_leve"]
    bank["fogo_suave"] = _write_wav(sfx_dir / "fogo.wav", noise_whoosh(2.0, 0.08, 700))
    bank["liquido"] = bank["agua"]
    bank["silencio"] = _write_wav(sfx_dir / "silencio.wav", np.zeros(int(0.4 * sr)))
    n = int(2 * sr)
    t = np.arange(n) / sr
    harm = (np.sin(2 * math.pi * 523 * t) + 0.5 * np.sin(2 * math.pi * 659 * t)) * np.hanning(n) * 0.12
    bank["harmonia"] = _write_wav(sfx_dir / "harmonia.wav", harm)
    return bank


def fit_cover(img: Image.Image, size: Tuple[int, int] = (WIDTH, HEIGHT)) -> Image.Image:
    tw, th = size
    w, h = img.size
    scale = max(tw / w, th / h)
    nw, nh = int(w * scale), int(h * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def grade_scene(img: Image.Image, act: str) -> Image.Image:
    img = img.convert("RGB")
    if act in ("abertura", "desenvolvimento"):
        img = ImageEnhance.Color(img).enhance(1.08)
        img = ImageEnhance.Contrast(img).enhance(1.05)
    elif act == "climax":
        img = ImageEnhance.Contrast(img).enhance(1.18)
        img = ImageEnhance.Color(img).enhance(1.12)
        img = ImageEnhance.Brightness(img).enhance(1.05)
    else:
        img = ImageEnhance.Color(img).enhance(1.1)
        img = ImageEnhance.Brightness(img).enhance(1.02)
    w, h = img.size
    overlay = Image.new("RGB", (w, h), (0, 0, 0))
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    for i in range(60):
        alpha = int(110 * ((60 - i) / 60) ** 1.8)
        draw.rectangle([i * 10, i * 6, w - i * 10, h - i * 6], outline=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(50))
    return Image.composite(overlay, img, mask)


def render_text_overlay(text: str, duration_hint: float = 3.0) -> Image.Image:
    return render_subtitle(text, style="title")


def render_subtitle(text: str, style: str = "subtitle") -> Image.Image:
    """Legenda em português para toda a cena (legível, com fundo semitransparente)."""
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    if style == "title":
        font = _load_font(52, bold=True)
        max_w = WIDTH * 0.82
        y_anchor = HEIGHT - 260
        panel_alpha = 140
    else:
        font = _load_font(40, bold=True)
        max_w = WIDTH * 0.88
        y_anchor = HEIGHT - 200
        panel_alpha = 160

    words = _sanitize_pt_text(text).split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    # no máximo 4 linhas
    if len(lines) > 4:
        lines = lines[:3] + [" ".join(lines[3:])]
        # rewrap last if needed roughly
        while len(lines) > 4:
            lines = lines[:3] + [" ".join(lines[3:])[:80] + "…"]

    line_h = 58 if style != "title" else 68
    total_h = len(lines) * line_h
    y0 = y_anchor - total_h // 2
    pad = 22
    panel = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle(
        [WIDTH * 0.05, y0 - pad, WIDTH * 0.95, y0 + total_h + pad],
        radius=16,
        fill=(0, 0, 0, panel_alpha),
    )
    overlay = Image.alpha_composite(overlay, panel)
    draw = ImageDraw.Draw(overlay)
    for i, line in enumerate(lines):
        tw = draw.textlength(line, font=font)
        x = (WIDTH - tw) / 2
        y = y0 + i * line_h
        draw.text((x + 2, y + 2), line, font=font, fill=(0, 0, 0, 200))
        draw.text((x, y), line, font=font, fill=(255, 248, 230, 255))
    return overlay


def generate_scene_images(scenes: List[Dict], images_dir: Path, seed: int) -> List[str]:
    from core.leonardo_client import LeonardoClient

    client = LeonardoClient()
    images_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for s in scenes:
        out = images_dir / f"scene_{s['num']:02d}.jpg"
        # reuse if present
        if out.exists() and out.stat().st_size > 20_000:
            logger.info("Cena %d já existe", s["num"])
            paths.append(str(out))
            continue
        # slight seed offset per scene but related for consistency
        scene_seed = seed + s["num"] * 17
        try:
            client.generate_to_file(
                s["prompt"],
                str(out),
                width=1472,
                height=832,
                seed=scene_seed,
            )
        except Exception as e:
            logger.error("Falha Leonardo cena %d: %s — usando fallback procedural", s["num"], e)
            _fallback_scene(str(out), s)
        # convert/grade to 1920x1080 jpeg
        img = Image.open(out).convert("RGB")
        img = fit_cover(img)
        img = grade_scene(img, s["act"])
        img.save(out, quality=92)
        paths.append(str(out))
        time.sleep(0.5)
    return paths


def _fallback_scene(path: str, scene: Dict) -> None:
    """Fallback visual se Leonardo falhar: gradiente cinematográfico + tipografia."""
    act = scene["act"]
    palettes = {
        "abertura": [(28, 42, 68), (180, 120, 60)],
        "desenvolvimento": [(24, 70, 48), (140, 170, 90)],
        "climax": [(12, 16, 40), (220, 170, 70)],
        "conclusao": [(40, 30, 60), (240, 160, 80)],
    }
    c0, c1 = palettes.get(act, [(20, 20, 30), (120, 100, 60)])
    img = Image.new("RGB", (WIDTH, HEIGHT))
    px = img.load()
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(c0[0] * (1 - t) + c1[0] * t)
        g = int(c0[1] * (1 - t) + c1[1] * t)
        b = int(c0[2] * (1 - t) + c1[2] * t)
        for x in range(WIDTH):
            px[x, y] = (r, g, b)
    draw = ImageDraw.Draw(img)
    font = _load_font(42, bold=True)
    label = f"Cena {scene['num']}: {scene['acao'][:60]}"
    draw.text((80, HEIGHT // 2), label, font=font, fill=(245, 236, 210))
    img.save(path, quality=90)


def compose_film(
    scenes: List[Dict],
    image_paths: List[str],
    voice_meta: List[Dict],
    music_path: str,
    sfx_bank: Dict[str, str],
    output_path: str,
) -> Dict[str, Any]:
    from moviepy.editor import (
        AudioFileClip,
        CompositeAudioClip,
        CompositeVideoClip,
        ImageClip,
        concatenate_audioclips,
        concatenate_videoclips,
    )
    from moviepy.video.fx.all import fadein, fadeout

    clips = []
    timeline = []
    t_cursor = 0.0
    # Timing por cena: início da voz e duração (para sincronizar legenda)
    scene_voice_plan = []

    for i, scene in enumerate(scenes):
        img_path = image_paths[i]
        voice = voice_meta[i]
        v_dur = float(voice["duration"])
        # Duração já calculada em ensure_min_duration (falada + folga curta)
        dur = float(scene["duration"])
        v_start = VOICE_START
        scene_voice_plan.append({"start": v_start, "duration": v_dur})

        src = Image.open(img_path).convert("RGB")
        big = fit_cover(src, (int(WIDTH * 1.22), int(HEIGHT * 1.22)))
        big_path = str(Path(img_path).with_name(f"_motion_{Path(img_path).name}"))
        big.save(big_path, quality=92)
        base = ImageClip(big_path).set_duration(dur)

        z0, z1 = (1.0, 1.12) if i % 2 == 0 else (1.10, 1.0)
        dx = 30 if i % 3 == 0 else (-28 if i % 3 == 1 else 16)
        dy = -18 if i % 2 == 0 else 22

        def make_resize(z_start, z_end, total):
            def _r(t):
                p = min(1.0, max(0.0, t / max(total, 0.01)))
                p = p * p * (3 - 2 * p)
                return z_start + (z_end - z_start) * p

            return _r

        try:
            base = base.resize(make_resize(z0, z1, dur))
            bw = int(WIDTH * 1.22)
            bh = int(HEIGHT * 1.22)

            def _pos(t, total=dur, ox=dx, oy=dy, ww=bw, hh=bh):
                p = min(1.0, max(0.0, t / max(total, 0.01)))
                p = p * p * (3 - 2 * p)
                return ((WIDTH - ww) / 2 + ox * p, (HEIGHT - hh) / 2 + oy * p)

            base = base.set_position(_pos)
        except Exception:
            base = base.set_position("center")

        layers = [base]

        # LEGENDAS sincronizadas exatamente com a narração da cena
        narr = scene.get("narracao") or ""
        title = scene.get("texto_tela")

        def _add_sub(text: str, start: float, length: float, style: str = "subtitle"):
            if not text or length <= 0.05:
                return
            ov = render_subtitle(text, style=style)
            ov_np = np.array(ov)
            rgb = ov_np[..., :3]
            mask = (ov_np[..., 3] / 255.0).astype(np.float32)
            length = min(length, max(0.1, dur - start))
            tc = (
                ImageClip(rgb)
                .set_duration(length)
                .set_start(start)
                .set_position((0, 0))
                .set_mask(ImageClip(mask, ismask=True).set_duration(length))
            )
            tc = tc.fx(fadein, min(0.12, length * 0.2)).fx(fadeout, min(0.15, length * 0.2))
            layers.append(tc)

        if title and scene["num"] in (1, 20):
            # Título curto antes; narração no tempo da voz
            title_len = min(1.6, max(0.8, v_start + 0.1))
            _add_sub(title, 0.05, title_len, style="title")
            _add_sub(narr, v_start, v_dur, style="subtitle")
        else:
            _add_sub(narr or title or "", v_start, v_dur, style="subtitle")

        scene_clip = CompositeVideoClip(layers, size=(WIDTH, HEIGHT)).set_duration(dur)
        fi = 0.35 if i == 0 else CROSSFADE
        scene_clip = scene_clip.fx(fadein, fi).fx(fadeout, CROSSFADE)
        clips.append(scene_clip)
        timeline.append({
            "num": scene["num"],
            "start": t_cursor,
            "duration": dur,
            "voice": voice["path"],
            "voice_start": v_start,
            "voice_duration": v_dur,
        })
        t_cursor += dur - CROSSFADE

    video = concatenate_videoclips(clips, method="compose", padding=-CROSSFADE)
    total = video.duration

    music = AudioFileClip(music_path).volumex(0.06)
    if music.duration < total:
        loops = int(math.ceil(total / music.duration))
        music = concatenate_audioclips([music] * loops).subclip(0, total)
    else:
        music = music.subclip(0, total)

    audio_layers = [music]
    t = 0.0
    for i, scene in enumerate(scenes):
        dur = clips[i].duration
        plan = scene_voice_plan[i]
        vclip = AudioFileClip(voice_meta[i]["path"]).volumex(1.2)
        # Mesmo offset usado nas legendas
        start = t + plan["start"]
        if start + vclip.duration > total:
            vclip = vclip.subclip(0, max(0.4, total - start))
        audio_layers.append(vclip.set_start(start))

        # SFX bem curtos e baixos (não no ataque da fala)
        for name in scene.get("sfx") or []:
            sp = sfx_bank.get(name)
            if not sp or name in ("silencio", "respiracao"):
                continue
            try:
                s_start = t + max(0.0, plan["start"] - 0.15)
                sclip = AudioFileClip(sp).volumex(0.06).set_start(s_start)
                if sclip.duration > 1.2:
                    sclip = sclip.subclip(0, 1.2)
                audio_layers.append(sclip)
            except Exception:
                pass
        t += dur - CROSSFADE

    final_audio = CompositeAudioClip(audio_layers).set_duration(total)
    final = video.set_audio(final_audio)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    logger.info("Exportando filme (%.1fs) → %s", total, output_path)
    final.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        bitrate="7000k",
        audio_bitrate="192k",
        preset="fast",
        threads=4,
        logger="bar",
    )
    final.close()
    video.close()
    for c in clips:
        c.close()

    return {"video_path": output_path, "duration_seconds": total, "timeline": timeline}


def ensure_min_duration(scenes: List[Dict], voice_meta: List[Dict], min_sec: float = 120.0) -> List[Dict]:
    """Duração por cena = fala + folga curta; só estica se total < 2 min."""
    durs = []
    for i, s in enumerate(scenes):
        d = voice_meta[i]["duration"] + VOICE_START + SCENE_TAIL
        durs.append(d)
        s["duration"] = d
    total = sum(durs) - CROSSFADE * (len(scenes) - 1)
    if total >= min_sec:
        return scenes
    # Distribui o mínimo necessário sem criar pausas grandes
    deficit = (min_sec - total) + 0.5
    extra = deficit / len(scenes)
    for i, s in enumerate(scenes):
        s["duration"] = durs[i] + extra
    return scenes


def run_narrative_salmo23_pipeline(
    output_dir: Optional[str] = None,
    skip_images: bool = False,
) -> Dict[str, Any]:
    from data.salmo23_narrative_film import (
        ANALYSIS,
        AUDIO_STRATEGY,
        CHARACTERS,
        NARRATION_FULL,
        PSALM_REF,
        PSALM_TEXT,
        SCENES,
        SEED,
    )

    root = _project_root()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(output_dir or (root / "outputs" / "narrative_film" / f"salmo23_{ts}"))
    out.mkdir(parents=True, exist_ok=True)

    scenes = [dict(s) for s in SCENES]
    write_docs(out, ANALYSIS, CHARACTERS, scenes, NARRATION_FULL)
    (out / "psalm.txt").write_text(PSALM_TEXT, encoding="utf-8")
    (out / "storyboard.json").write_text(json.dumps(scenes, ensure_ascii=False, indent=2), encoding="utf-8")

    logger.info("=== FILME NARRATIVO %s ===", PSALM_REF)
    logger.info("Pasta: %s", out)

    # 1) Images
    images_dir = out / "scenes"
    if skip_images and all((images_dir / f"scene_{s['num']:02d}.jpg").exists() for s in scenes):
        image_paths = [str(images_dir / f"scene_{s['num']:02d}.jpg") for s in scenes]
    else:
        image_paths = generate_scene_images(scenes, images_dir, SEED)

    # 2) Voices
    voice_meta = generate_scene_voices(scenes, out / "audio" / "voice")
    scenes = ensure_min_duration(scenes, voice_meta, min_sec=125.0)

    # 3) Score + SFX
    # provisional total for score length
    approx = sum(max(s["duration"], 6.5) for s in scenes) - CROSSFADE * (len(scenes) - 1)
    music_path = synthesize_score(approx + 5, out / "audio" / "score.wav")
    sfx_bank = synthesize_sfx_bank(out / "audio" / "sfx")

    # 4) Compose
    video_path = str(out / f"salmo23_narrative_film_{ts}.mp4")
    result = compose_film(scenes, image_paths, voice_meta, music_path, sfx_bank, video_path)

    # 5) Verify duration
    real_dur = _ffprobe_duration(video_path)
    result["duration_seconds"] = real_dur
    result["output_dir"] = str(out)
    result["psalm"] = PSALM_REF
    (out / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if real_dur < 120:
        logger.warning("Duração %.1fs < 120s — considere reexecutar com padding", real_dur)
    else:
        logger.info("OK: duração %.1fs (≥ 2 min)", real_dur)
    logger.info("Vídeo final: %s", video_path)
    return result


if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(_project_root()))
    from dotenv import load_dotenv

    load_dotenv(_project_root() / ".env")
    run_narrative_salmo23_pipeline()
