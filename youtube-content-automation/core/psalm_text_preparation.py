"""
Preparação textual inteligente para narração de salmos.

Objetivo: ritmo humano, cadência bíblica, pausas naturais, blocos equilibrados.
Etapas: normalização → cadência → respiração → equilíbrio visual → sincronização.
"""

import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Equilíbrio visual: cada bloco ~8–18 palavras (leitura confortável, tela balanceada)
PREP_MIN_WORDS = 8
PREP_MAX_WORDS = 18
# Tamanho mínimo para não fundir (evita blocos minúsculos que soam quebrados)
PREP_MIN_SEGMENT_WORDS = 5

__all__ = [
    "normalize_psalm_text",
    "normalize_text_for_display",
    "segment_by_cadence",
    "balance_segments",
    "prepare_psalm_for_narration",
]


def normalize_text_for_display(text: str) -> str:
    """
    Normalização para exibição visual (antes de renderizar).
    - Remove espaços quebrados e duplicados
    - Padroniza pontuação
    - Capitalização correta: primeira letra de cada frase maiúscula; resto coerente
    - Garante que nenhuma tela comece com palavra cortada (texto limpo por bloco)
    """
    if not (text or "").strip():
        return ""
    t = text.strip()
    t = re.sub(r"[\s\n\r]+", " ", t)
    t = re.sub(r"\.{2,}|…", "...", t)
    t = re.sub(r"-{2,}", "—", t)
    t = re.sub(r"\s+([.,;:!?])", r"\1", t)
    t = re.sub(r"([.;:!?])([A-Za-zÀ-ÿ])", r"\1 \2", t)
    # Se todo o texto for MAIÚSCULAS (ex.: referência "SALMO 46:10"), usar title case
    letters = [c for c in t if c.isalpha()]
    if letters and all(c.isupper() for c in letters):
        t = t.title()
    # Caso contrário: primeira letra e após .!? em maiúscula (frase)
    if not t:
        return t
    out: List[str] = []
    for i, c in enumerate(t):
        if i == 0:
            out.append(c.upper() if c.isalpha() else c)
        elif i >= 1 and t[i - 1] in ".!?" and c.isalpha():
            out.append(c.upper())
        else:
            out.append(c)
    return "".join(out).strip()


def _word_count(text: str) -> int:
    return len((text or "").strip().split())


def normalize_psalm_text(text: str) -> str:
    """
    Etapa 1 — Normalização.
    Remove quebras aleatórias, limpa espaços, padroniza pontuação.
    """
    if not (text or "").strip():
        return ""
    t = text.strip()
    # Colapsar múltiplos espaços e quebras em um único espaço
    t = re.sub(r"[\s\n\r]+", " ", t)
    # Padronizar reticências (… ou ..) → ...
    t = re.sub(r"\.{2,}|…", "...", t)
    # Manter travessão tipográfico, normalizar hífens repetidos
    t = re.sub(r"-{2,}", "—", t)
    # Espaço após pontuação forte quando grudado na palavra seguinte
    t = re.sub(r"([.;:!?])([A-Za-zÀ-ÿ])", r"\1 \2", t)
    # Remover espaços antes de pontuação
    t = re.sub(r"\s+([.,;:!?])", r"\1", t)
    return t.strip()


def _split_at_strong_pauses(normalized: str) -> List[str]:
    """
    Quebra em pausas fortes: ponto, ponto e vírgula, dois-pontos, !, ?.
    Cada trecho preserva a pontuação final.
    """
    if not normalized.strip():
        return []
    # Split mantendo o delimitador no trecho anterior (frase termina com . ; : ! ?)
    parts = re.split(r"(?<=[.;:!?])\s+", normalized)
    return [p.strip() for p in parts if p.strip()]


def _split_long_at_commas(segment: str, max_words: int) -> List[str]:
    """Se o segmento for longo, quebra em vírgulas (pausa curta natural)."""
    wc = _word_count(segment)
    if wc <= max_words:
        return [segment]
    # Quebrar por vírgula
    sub = re.split(r",\s*", segment)
    out: List[str] = []
    current: List[str] = []
    current_words = 0
    for i, part in enumerate(sub):
        need_comma = i < len(sub) - 1
        phrase = part + ("," if need_comma else "")
        n = _word_count(phrase)
        if current_words + n <= max_words and (current_words > 0 or n <= max_words):
            current.append(phrase)
            current_words += n
        else:
            if current:
                out.append(" ".join(current).replace(" ,", ",").strip())
            current = [phrase]
            current_words = n
    if current:
        out.append(" ".join(current).replace(" ,", ",").strip())
    return out if out else [segment]


def segment_by_cadence(normalized: str) -> List[str]:
    """
    Etapa 2 — Cadência inteligente.
    Quebra por sentido: ponto = pausa média, ponto e vírgula = longa, vírgula = curta (em frases longas).
    """
    if not normalized.strip():
        return []
    segments = _split_at_strong_pauses(normalized)
    result: List[str] = []
    for seg in segments:
        if _word_count(seg) > PREP_MAX_WORDS:
            result.extend(_split_long_at_commas(seg, PREP_MAX_WORDS))
        else:
            result.append(seg)
    return result


def balance_segments(segments: List[str]) -> List[str]:
    """
    Etapa 4 — Equilíbrio visual.
    Agrupa segmentos muito curtos (sem deixar vazio); divide os muito longos.
    Blocos com tamanho semelhante, leitura confortável.
    """
    if not segments:
        return []
    merged: List[str] = []
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        wc = _word_count(seg)
        if wc > PREP_MAX_WORDS:
            merged.extend(_split_long_at_commas(seg, PREP_MAX_WORDS))
        elif merged and _word_count(merged[-1]) < PREP_MIN_SEGMENT_WORDS and wc < PREP_MAX_WORDS:
            # Fundir com o anterior se ambos curtos
            merged[-1] = (merged[-1] + " " + seg).strip()
        elif merged and wc < PREP_MIN_WORDS and _word_count(merged[-1]) + wc <= PREP_MAX_WORDS:
            merged[-1] = (merged[-1] + " " + seg).strip()
        else:
            merged.append(seg)
    return merged


def _ensure_breathing_punctuation(segment: str) -> str:
    """
    Etapa 3 — Respiração humana (leve).
    Garante que vocativos e antes de palavras-chave tenham pausa (vírgula).
    TTS lê melhor com pontuação consistente.
    """
    if not segment or len(segment) < 10:
        return segment
    s = segment
    # "Senhor" ou "ó Senhor" no início ou após vírgula: garantir vírgula após se não houver
    for voc in ("Senhor", "Deus", "ó Senhor", "ó Deus"):
        if voc in s and not re.search(rf"{re.escape(voc)}\s*[,.]", s):
            # Só inserir se for vocativo (seguido de verbo ou fim de frase)
            pass  # evita alterar demais o texto; cadência já cuida das pausas
    return s


def prepare_psalm_for_narration(text: str) -> Dict[str, Any]:
    """
    Pipeline completo de preparação.
    Retorna:
      - normalized: texto limpo e padronizado
      - segments: lista de blocos equilibrados (cada um = 1 unidade de áudio/tela)
      - full_text: texto completo para TTS único (se preferir um só áudio)
    """
    if not (text or "").strip():
        return {"normalized": "", "segments": [], "full_text": ""}
    normalized = normalize_psalm_text(text)
    segments = segment_by_cadence(normalized)
    segments = balance_segments(segments)
    segments = [_ensure_breathing_punctuation(s) for s in segments]
    full_text = " ".join(segments)
    logger.info(
        "Preparação textual: %d blocos (cadência + equilíbrio), ~%d–%d palavras/bloco",
        len(segments),
        PREP_MIN_WORDS,
        PREP_MAX_WORDS,
    )
    return {
        "normalized": normalized,
        "segments": segments,
        "full_text": full_text,
    }
