"""
Data modules: Salmos (150 no livro) e passagens da Bíblia.
"""

from .salmos_completos import (
    TOTAL_SALMOS,
    SALMOS_COMPLETOS,
    MOOD_TO_PALETTE,
    get_salmo_by_name,
    get_salmo_by_index,
    get_salmo_by_number,
    get_palette_for_salmo,
    list_all_salmos,
)
from .passagens_biblia import (
    PASSAGENS_BIBLIA,
    get_passagem_by_index,
    get_passagem_by_referencia,
    get_palette_for_passagem,
    list_all_passagens,
)

__all__ = [
    "TOTAL_SALMOS",
    "SALMOS_COMPLETOS",
    "MOOD_TO_PALETTE",
    "get_salmo_by_name",
    "get_salmo_by_index",
    "get_salmo_by_number",
    "get_palette_for_salmo",
    "list_all_salmos",
    "PASSAGENS_BIBLIA",
    "get_passagem_by_index",
    "get_passagem_by_referencia",
    "get_palette_for_passagem",
    "list_all_passagens",
]
