"""
Descrições otimizadas por rede social para o Salmo do Dia.

Gera automaticamente descrições para: YouTube, Instagram, Twitter, TikTok,
Facebook, Threads, Pinterest e Telegram — com tom viral, hashtags e CTA por plataforma.
Identidade espiritual moderna, linguagem natural.
"""

import os
from typing import Dict, List, Optional

# Hashtags em formato texto; ao gerar, usar .replace(" ", "") para o hashtag (#salmododia)
HASHTAGS_SALMO_DIA = [
    "salmo do dia",
    "salmo de hoje",
    "palavra do dia",
    "mensagem de deus",
    "versiculo do dia",
    "biblia sagrada",
    "salmos",
    "oração do dia",
    "oração poderosa",
    "deus",
    "jesus",
    "espirito santo",
    "fé",
    "palavra de deus",
    "evangelho",
    "salmo 23",
    "salmo 91",
    "oração da manhã",
    "oração da noite",
    "oração para dormir",
    "oração para proteção",
    "oração milagrosa",
    "shorts",
    "youtube shorts",
    "viral",
    "reflexão",
    "mensagem motivacional",
    "brasil",
    "português",
]


def _hashtag_line(tags: List[str], limit: Optional[int] = None) -> str:
    """Junta tags em linha de hashtags (sem espaços)."""
    normalized = [t.replace(" ", "") for t in tags]
    if limit is not None:
        normalized = normalized[:limit]
    return " ".join(f"#{t}" for t in normalized)


def _first_sentence(text: str, max_chars: int = 120) -> str:
    """Extrai a primeira frase ou trecho impactante do texto (para hooks)."""
    text = " ".join((text or "").strip().split())
    if not text:
        return ""
    for sep in ".!?":
        idx = text.find(sep)
        if idx != -1:
            out = text[: idx + 1].strip()
            return out[:max_chars] if len(out) > max_chars else out
    return text[:max_chars].strip() + ("..." if len(text) > max_chars else "")


def _first_line_short(text: str, max_chars: int = 80) -> str:
    """Primeira linha ou trecho curto para Twitter/TikTok."""
    line = (text or "").strip().split("\n")[0].strip()
    line = " ".join(line.split())
    if len(line) <= max_chars:
        return line
    return line[: max_chars - 3].rsplit(" ", 1)[0] + "..."


def _viral_caption(psalm_name: str, body_text: str) -> str:
    """
    Gera bloco de legenda no estilo viral: citação, não é por acaso, reflexão, CTA e engajamento.
    """
    quote = _first_sentence(body_text, 100).strip()
    if not quote:
        quote = "Uma palavra para o seu dia."
    if not quote.endswith(("…", ".", "!", "?")):
        quote = quote + "…"
    lines = [
        f'"{quote}" ❤️',
        "",
        f"📖 {psalm_name}",
        "",
        "Se essa mensagem chegou até você hoje… não é por acaso.",
        "Deus está te lembrando de algo simples, mas poderoso.",
        "",
        "Mesmo quando for difícil… Mesmo quando doer… Deus está com você.",
        "",
        "🤍 Guarde essa palavra no coração hoje.",
        "",
        "🔥 Comenta \"AMÉM\" se você crê",
        "💬 Você já sentiu isso na sua vida?",
        "",
        "Segue para receber a Palavra todos os dias 🙌",
    ]
    return "\n".join(lines)


def _viral_caption_youtube(psalm_name: str, body_text: str) -> str:
    """
    Versão para YouTube: reflexiva e amigável às regras da plataforma.
    Sem CTAs repetitivos de engajamento (evita "comenta AMÉM", etc.) para não ser visto como engagement bait.
    """
    quote = _first_sentence(body_text, 100).strip()
    if not quote:
        quote = "Uma palavra para o seu dia."
    if not quote.endswith(("…", ".", "!", "?")):
        quote = quote + "…"
    lines = [
        f'"{quote}"',
        "",
        f"📖 {psalm_name}",
        "",
        "Se essa mensagem chegou até você hoje, que ela acompanhe o seu dia.",
        "Deus está com você.",
        "",
        "Inscreva-se no canal e ative o sininho para não perder os próximos vídeos.",
        "Salmos e passagens da Bíblia para inspirar e refletir.",
    ]
    return "\n".join(lines)


def generate_youtube_description(psalm_name: str, body_text: str) -> str:
    """
    Descrição para YouTube: reflexiva, dentro das regras (sem engagement bait).
    CTA discreto (inscreva-se/ative o sininho). Hashtags para SEO.
    """
    body = _viral_caption_youtube(psalm_name, body_text)
    hashtag_line = _hashtag_line(HASHTAGS_SALMO_DIA, limit=30)
    return f"{body}\n\n{hashtag_line}"


def generate_instagram_description(psalm_name: str, body_text: str) -> str:
    """
    Instagram: estilo viral, emocional, incentivo a salvar/compartilhar. Muitas hashtags.
    """
    viral = _viral_caption(psalm_name, body_text)
    viral += "\n\nSalve este post para ler de novo quando precisar de paz. 💛"
    hashtag_line = _hashtag_line(HASHTAGS_SALMO_DIA, limit=30)
    return f"{viral}\n\n{hashtag_line}"


def generate_twitter_description(psalm_name: str, body_text: str) -> str:
    """
    Twitter/X: até 280 caracteres (limite da plataforma). Curto e impactante.
    """
    TWITTER_MAX = 280
    quote = _first_line_short(body_text, 100)
    if not quote:
        quote = "Uma palavra para o seu dia."
    if not quote.endswith(("…", ".", "!", "?")):
        quote = quote + "…"
    # Texto principal: citação + referência (deixar espaço para hashtags)
    hashtag_line = _hashtag_line(HASHTAGS_SALMO_DIA, limit=5)
    base = f'"{quote}" 📖 {psalm_name}\n\n{hashtag_line}'
    if len(base) <= TWITTER_MAX:
        return base
    # Encurta a citação até caber
    for max_quote in (80, 60, 40):
        quote = _first_line_short(body_text, max_quote)
        if not quote.endswith(("…", ".", "!", "?")):
            quote = quote + "…"
        base = f'"{quote}" 📖 {psalm_name}\n\n{hashtag_line}'
        if len(base) <= TWITTER_MAX:
            return base
    # Último recurso: só referência + hashtags
    fallback = f"📖 {psalm_name}\n\n{hashtag_line}"
    return fallback[:TWITTER_MAX]


def generate_tiktok_description(psalm_name: str, body_text: str) -> str:
    """
    TikTok: estilo viral, hook forte, CTA para seguir e comentar AMÉM. Muitas hashtags.
    """
    viral = _viral_caption(psalm_name, body_text)
    hashtag_line = _hashtag_line(HASHTAGS_SALMO_DIA, limit=30)
    return f"{viral}\n\n{hashtag_line}"


def generate_facebook_description(psalm_name: str, body_text: str) -> str:
    """
    Facebook Reels: estilo viral, tom comunitário, incentivo a compartilhar. Muitas hashtags.
    """
    viral = _viral_caption(psalm_name, body_text)
    viral += "\n\nCompartilhe com quem precisa ouvir isso hoje. 🙏"
    hashtag_line = _hashtag_line(HASHTAGS_SALMO_DIA, limit=30)
    return f"{viral}\n\n{hashtag_line}"


def generate_threads_description(psalm_name: str, body_text: str) -> str:
    """
    Threads: estilo viral, tom conversacional. Hashtags moderadas.
    """
    quote = _first_sentence(body_text, 90)
    if not quote:
        quote = "Uma palavra para o seu dia."
    if not quote.endswith(("…", ".", "!", "?")):
        quote = quote + "…"
    lines = [
        f'"{quote}" ❤️',
        f"📖 {psalm_name}",
        "",
        "Se essa mensagem chegou até você hoje… não é por acaso. Comenta AMÉM se você crê 🙌",
    ]
    body = "\n".join(lines)
    hashtag_line = _hashtag_line(HASHTAGS_SALMO_DIA, limit=12)
    return f"{body}\n\n{hashtag_line}"


def generate_pinterest_description(psalm_name: str, body_text: str) -> str:
    """
    Pinterest: estilo viral, SEO espiritual. Muitas hashtags.
    """
    viral = _viral_caption(psalm_name, body_text)
    viral += "\n\nSalve no seu quadro e volte quando precisar de inspiração."
    hashtag_line = _hashtag_line(HASHTAGS_SALMO_DIA, limit=25)
    return f"{viral}\n\n{hashtag_line}"


def generate_telegram_description(psalm_name: str, body_text: str) -> str:
    """
    Telegram: estilo viral, tom íntimo. Hashtags moderadas.
    """
    viral = _viral_caption(psalm_name, body_text)
    hashtag_line = _hashtag_line(HASHTAGS_SALMO_DIA, limit=15)
    return f"{viral}\n\n{hashtag_line}"


def save_descriptions(
    output_dir: str,
    psalm_name: str,
    body_text: str,
) -> Dict[str, str]:
    """
    Gera e grava descrições para todas as plataformas na pasta output_dir:
    youtube.txt, instagram.txt, twitter.txt, tiktok.txt, facebook.txt,
    threads.txt, pinterest.txt, telegram.txt.
    Retorna dict com paths dos arquivos criados.
    """
    os.makedirs(output_dir, exist_ok=True)
    paths = {}
    generators = [
        ("youtube.txt", generate_youtube_description),
        ("instagram.txt", generate_instagram_description),
        ("twitter.txt", generate_twitter_description),
        ("tiktok.txt", generate_tiktok_description),
        ("facebook.txt", generate_facebook_description),
        ("threads.txt", generate_threads_description),
        ("pinterest.txt", generate_pinterest_description),
        ("telegram.txt", generate_telegram_description),
    ]
    for filename, generate_fn in generators:
        content = generate_fn(psalm_name, body_text or "")
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        paths[filename.replace(".txt", "")] = filepath
    return paths
