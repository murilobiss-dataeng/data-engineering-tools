"""
Utilitários de publicação: tags automáticas, capítulos na descrição, hash anti-repost.

- Tags: gerar lista a partir do título + tema do vídeo.
- Capítulos: adicionar timestamps na descrição para chapters/key moments automáticos.
- Content hash: hash(title + texto + script) para bloquear repostagem do mesmo conteúdo.
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import List, Optional


def generate_tags_from_title_and_theme(
    title: str,
    theme: str = "",
    max_tags: int = 30,
    extra_keywords: Optional[List[str]] = None,
) -> List[str]:
    """
    Gera lista de tags com base no título e no tema do vídeo.
    Extrai palavras significativas (sem acentos para padrão) e combina com tema e extras.
    """
    seen = set()
    tags: List[str] = []

    def add(t: str) -> None:
        t = (t or "").strip().lower()
        if not t or len(t) < 2:
            return
        # normaliza para comparação (evita duplicatas por acento)
        key = re.sub(r"[^\w\s]", "", t).strip()
        if key and key not in seen:
            seen.add(key)
            tags.append(t[:100])

    # Tema como tag principal
    if theme:
        for w in theme.replace(",", " ").split():
            add(w)

    # Palavras do título (ignora stopwords comuns)
    stop = {"do", "da", "de", "di", "du", "e", "o", "a", "os", "as", "um", "uma", "em", "no", "na", "com", "para", "por", "que", "|"}
    for w in re.findall(r"\b[\w']+\b", (title or "").lower()):
        if w not in stop and len(w) > 1:
            add(w)

    # Extras (ex.: palavras-chave do canal)
    for w in extra_keywords or []:
        add(w)

    return tags[:max_tags]


def build_description_with_chapters(
    description: str,
    duration_estimate_sec: float,
    intro_label: str = "Introdução",
    main_label: str = "Conteúdo principal",
    end_label: str = "Conclusão",
) -> str:
    """
    Adiciona seção de capítulos na descrição para ativar chapters/key moments no YouTube.
    YouTube usa timestamps no formato 0:00 ou 0:00:00 na descrição.
    """
    if duration_estimate_sec < 10:
        return description
    intro_end = min(5, int(duration_estimate_sec * 0.15))
    main_end = max(intro_end + 5, int(duration_estimate_sec * 0.85))

    def ts(sec: int) -> str:
        if sec >= 3600:
            return f"{sec // 3600}:{(sec % 3600) // 60:02d}:{sec % 60:02d}"
        return f"{sec // 60}:{sec % 60:02d}"

    lines = [
        description.strip(),
        "",
        "--- Capítulos ---",
        f"0:00 {intro_label}",
        f"{ts(intro_end)} {main_label}",
        f"{ts(main_end)} {end_label}",
    ]
    return "\n".join(lines)


def content_hash(title: str, text: str, script: str = "") -> str:
    """Hash único do conteúdo (título + texto + script) para detectar repostagem."""
    payload = f"{title}|{text}|{script}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class ContentHashStorage:
    """
    Armazena hashes de conteúdo já publicados por canal.
    Uso: antes de postar, verificar is_duplicate(h); após postar com sucesso, save_hash(h).
    """

    def __init__(self, channel_namespace: str, base_dir: str = "outputs"):
        self.channel_namespace = channel_namespace
        self.base_dir = Path(base_dir)
        self._storage_dir = self.base_dir / channel_namespace / "storage"
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        self._file = self._storage_dir / "content_hashes.json"

    def _load(self) -> List[str]:
        if not self._file.exists():
            return []
        try:
            with open(self._file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("hashes", [])
        except Exception:
            return []

    def _save(self, hashes: List[str]) -> None:
        with open(self._file, "w", encoding="utf-8") as f:
            json.dump({"hashes": hashes, "channel": self.channel_namespace}, f, indent=2)

    def is_duplicate(self, content_hash: str) -> bool:
        return content_hash in self._load()

    def save_hash(self, content_hash: str) -> None:
        hashes = self._load()
        if content_hash not in hashes:
            hashes.append(content_hash)
            self._save(hashes)
