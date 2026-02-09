"""
Descrições otimizadas por rede social para o Salmo do Dia.

Gera automaticamente descrições para: YouTube, Instagram, Twitter, TikTok,
Facebook, Threads, Pinterest e Telegram — com tom, hashtags e CTA por plataforma.
Identidade espiritual moderna, linguagem natural.
"""

import os
from typing import Dict, List


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


def generate_youtube_description(psalm_name: str, body_text: str) -> str:
    """
    Descrição para YouTube: 2–3 parágrafos, reflexiva, SEO bíblico.
    Call to action: curtir, comentar, inscrever-se. 5–8 hashtags no final.
    """
    intro = (
        f"📖 {psalm_name}\n\n"
        "Uma palavra para o seu dia. Este salmo nos convida à reflexão e ao encontro com Deus.\n\n"
    )
    # Breve contexto: primeiras linhas do salmo como “resumo”
    first = _first_sentence(body_text, 200)
    if first:
        intro += f'"{first}"\n\n'
    outro = (
        "Se este vídeo falou ao seu coração, deixe seu like e um comentário. "
        "Inscreva-se no canal e ative o sininho para não perder os próximos Salmos do Dia.\n\n"
        "🙏 Salmos e passagens da Bíblia para inspirar o seu dia."
    )
    hashtags = [
        "salmo",
        "bíblia",
        "palavradeDeus",
        "reflexão",
        "fé",
        "espiritualidade",
        "oração",
        "cristão",
    ]
    hashtag_line = " ".join(f"#{t}" for t in hashtags[:8])
    return f"{intro}{outro}\n\n{hashtag_line}"


def generate_instagram_description(psalm_name: str, body_text: str) -> str:
    """
    Texto emocional para Instagram: quebras de linha, emojis sutis.
    Incentivo a salvar/compartilhar. 8–12 hashtags. Foco em inspiração.
    """
    hook = _first_sentence(body_text, 100)
    lines = [
        f"📖 {psalm_name}",
        "",
        hook if hook else "Uma palavra para o seu dia.",
        "",
        "Salve este post para ler de novo quando precisar de paz. 💛",
        "Compartilhe com quem precisa ouvir isso hoje.",
        "",
        "— Salmo do Dia",
    ]
    hashtags = [
        "salmo",
        "bíblia",
        "palavradeDeus",
        "fé",
        "espiritualidade",
        "oração",
        "cristão",
        "reflexão",
        "inspiração",
        "meditação",
        "palavra",
        "jesus",
    ]
    body = "\n".join(lines)
    hashtag_line = " ".join(f"#{t}" for t in hashtags[:12])
    return f"{body}\n\n{hashtag_line}"


def generate_twitter_description(psalm_name: str, body_text: str) -> str:
    """
    Twitter/X: curto e impactante. Frase central do salmo. 2–4 hashtags. Linguagem direta.
    """
    central = _first_line_short(body_text, 80)
    if not central:
        central = f"{psalm_name} — uma palavra para o seu dia."
    line = f'"{central}"'
    if len(line) > 200:
        line = line[:197] + "..."
    hashtags = ["salmo", "bíblia", "palavradeDeus", "fé"]
    hashtag_line = " ".join(f"#{t}" for t in hashtags[:4])
    return f"{line}\n\n{psalm_name}\n\n{hashtag_line}"


def generate_tiktok_description(psalm_name: str, body_text: str) -> str:
    """
    TikTok: hook forte na primeira linha, conversacional, retenção.
    Chamada para seguir. 5–8 hashtags. Tom jovem mas respeitoso.
    """
    hook = _first_line_short(body_text, 70)
    if not hook:
        hook = "Uma palavra que pode mudar o seu dia."
    lines = [
        hook,
        "",
        f"📖 {psalm_name}",
        "",
        "Se isso falou com você, segue aqui para mais Salmos do Dia. 🙏",
        "Comenta o que mais te tocou.",
    ]
    hashtags = [
        "salmo",
        "bíblia",
        "palavradeDeus",
        "fé",
        "espiritualidade",
        "salmododia",
        "cristão",
        "oração",
    ]
    body = "\n".join(lines)
    hashtag_line = " ".join(f"#{t}" for t in hashtags[:8])
    return f"{body}\n\n{hashtag_line}"


def generate_facebook_description(psalm_name: str, body_text: str) -> str:
    """
    Facebook Reels: texto inspirador, tom comunitário.
    Incentivo a compartilhar. 5–8 hashtags.
    """
    hook = _first_sentence(body_text, 120)
    lines = [
        f"📖 {psalm_name}",
        "",
        hook if hook else "Uma palavra para o seu dia.",
        "",
        "Compartilhe com sua família e amigos. Que essa mensagem alcance quem precisa.",
        "Deixe um comentário contando o que esse salmo significa para você. 🙏",
        "",
        "— Salmo do Dia",
    ]
    hashtags = [
        "salmo",
        "bíblia",
        "palavradeDeus",
        "fé",
        "espiritualidade",
        "oração",
        "cristão",
        "comunidade",
    ]
    body = "\n".join(lines)
    hashtag_line = " ".join(f"#{t}" for t in hashtags[:8])
    return f"{body}\n\n{hashtag_line}"


def generate_threads_description(psalm_name: str, body_text: str) -> str:
    """
    Threads: frase reflexiva, tom humano e conversacional.
    Poucas hashtags (1–3).
    """
    central = _first_sentence(body_text, 100)
    if not central:
        central = "Uma palavra para o seu dia."
    lines = [
        f'"{central}"',
        "",
        f"— {psalm_name}",
        "",
        "O que esse trecho falou pra você?",
    ]
    hashtags = ["salmo", "bíblia", "fé"]
    body = "\n".join(lines)
    hashtag_line = " ".join(f"#{t}" for t in hashtags[:3])
    return f"{body}\n\n{hashtag_line}"


def generate_pinterest_description(psalm_name: str, body_text: str) -> str:
    """
    Pinterest: descrição inspiracional, SEO espiritual.
    Palavras-chave bíblicas. 5–10 hashtags.
    """
    hook = _first_sentence(body_text, 150)
    lines = [
        f"{psalm_name} — uma palavra para inspirar o seu dia.",
        "",
        hook if hook else "Salmos e passagens da Bíblia para reflexão e paz.",
        "",
        "Salve no seu quadro e volte quando precisar de inspiração. "
        "Ideal para meditação, devocional e momentos de quietude.",
    ]
    hashtags = [
        "salmo",
        "bíblia",
        "palavradeDeus",
        "fé",
        "espiritualidade",
        "oração",
        "meditação",
        "devocional",
        "reflexão",
        "cristão",
    ]
    body = "\n".join(lines)
    hashtag_line = " ".join(f"#{t}" for t in hashtags[:10])
    return f"{body}\n\n{hashtag_line}"


def generate_telegram_description(psalm_name: str, body_text: str) -> str:
    """
    Telegram: mensagem limpa, estilo devocional.
    Sem excesso de hashtags. Tom íntimo e contemplativo.
    """
    hook = _first_sentence(body_text, 130)
    lines = [
        f"📖 {psalm_name}",
        "",
        hook if hook else "Uma palavra para o seu dia.",
        "",
        "Que essa mensagem acompanhe você hoje.",
        "",
        "— Salmo do Dia",
    ]
    hashtags = ["salmo", "bíblia", "fé"]
    body = "\n".join(lines)
    hashtag_line = " ".join(f"#{t}" for t in hashtags[:3])
    return f"{body}\n\n{hashtag_line}"


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
