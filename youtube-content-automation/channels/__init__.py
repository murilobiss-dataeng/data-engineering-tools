"""
Channel processors for content generation.

Canais disponíveis (config em config/channels.yaml e config/templates_<id>.yaml):
  - salmo_dia: Salmo do Dia (salmos + passagens da Bíblia em um só canal)
  - curiosidade_dia, dica_carreira_dia, exercicio_dia, explicado_shorts,
  - motivacao_dia, placar_dia, quanto_rende, receita_dia, series_explicadas
"""

from .salmo_dia.channel_processor import SalmoDiaProcessor

__all__ = ["SalmoDiaProcessor"]
