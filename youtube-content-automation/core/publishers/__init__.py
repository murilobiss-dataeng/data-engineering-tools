"""
Publishers - Upload para múltiplos destinos.

Destinos suportados:
  - youtube   YouTube (Shorts)
  - twitter    Twitter/X
  - kwai       Kwai
  - instagram  Instagram (Reels) — alias: ig
  - tiktok     TikTok
  - facebook   Facebook (Reels/Vídeo) — alias: fb
  - linkedin   LinkedIn
"""

from .base import BasePublisher
from .dispatcher import (
    DESTINATIONS,
    DESTINATION_NAMES,
    get_available_destinations,
    get_configured_destinations,
    parse_destinations,
    publish_to_destinations,
)

__all__ = [
    "BasePublisher",
    "DESTINATIONS",
    "DESTINATION_NAMES",
    "get_available_destinations",
    "get_configured_destinations",
    "parse_destinations",
    "publish_to_destinations",
]
