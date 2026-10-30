"""
Pinterest Publisher - Criação de Pins de vídeo (Pinterest API v5).

A API v5 exige URL pública do vídeo (não envia arquivo local). Opções:
- Envie o vídeo para S3/Cloudinary/etc. e passe video_url nos kwargs, ou
- Use integração que publique primeiro no YouTube e use a URL do Short.

Requer: App em developers.pinterest.com, OAuth 2.0.
Variáveis de ambiente: PINTEREST_ACCESS_TOKEN, PINTEREST_BOARD_ID
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

from .base import BasePublisher

logger = logging.getLogger(__name__)


class PinterestPublisher(BasePublisher):
    """Cria Pins de vídeo no Pinterest (API v5; vídeo deve ter URL pública)."""

    id = "pinterest"
    name = "Pinterest"

    def __init__(self):
        self._access_token = os.getenv("PINTEREST_ACCESS_TOKEN")
        self._board_id = os.getenv("PINTEREST_BOARD_ID")

    @property
    def is_configured(self) -> bool:
        return bool(self._access_token and self._board_id)

    def publish(
        self,
        video_path: str,
        title: str,
        description: str = "",
        content_name: str = "",
        channel_label: str = "Salmo do Dia",
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Optional[Dict[str, Any]]:
        if not self.is_configured:
            return None
        # API v5: create pin com media_source = video_url (URL pública)
        video_url = kwargs.get("video_url") or kwargs.get("pinterest_video_url")
        if not video_url:
            logger.warning("Pinterest: API v5 exige URL pública do vídeo. Use video_url (ex.: após publicar no YouTube).")
            return None
        try:
            import requests
            headers = {"Authorization": f"Bearer {self._access_token}", "Content-Type": "application/json"}
            payload = {
                "board_id": self._board_id,
                "title": (title or content_name or "Pin")[:100],
                "description": (description or f"{content_name} | {channel_label}")[:500],
                "media_source": {"source_type": "video_url", "url": video_url},
            }
            r = requests.post(
                "https://api.pinterest.com/v5/pins",
                headers=headers,
                json=payload,
                timeout=60,
            )
            if r.ok:
                j = r.json()
                return {"id": j.get("id"), "url": j.get("link"), "platform": "pinterest"}
            logger.warning("Pinterest create pin: %s %s", r.status_code, r.text[:200])
        except Exception as e:
            logger.warning("Pinterest upload: %s", e)
        return None
