"""
Instagram Publisher - Upload de Reels para Instagram (Meta Graph API).

Requer: App Facebook/Instagram Developer, Instagram Business ou Creator account.
Documentação: https://developers.facebook.com/docs/instagram-api/
Variáveis de ambiente: META_APP_ID, META_APP_SECRET, INSTAGRAM_ACCESS_TOKEN (long-lived)
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List

from .base import BasePublisher


class InstagramPublisher(BasePublisher):
    """Upload de Reels para Instagram via Meta Graph API."""

    id = "instagram"
    name = "Instagram"

    def __init__(self):
        self._app_id = os.getenv("META_APP_ID") or os.getenv("FACEBOOK_APP_ID")
        self._app_secret = os.getenv("META_APP_SECRET") or os.getenv("FACEBOOK_APP_SECRET")
        self._access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN") or os.getenv("META_ACCESS_TOKEN")

    @property
    def is_configured(self) -> bool:
        return bool(self._access_token)

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
        # Instagram Content Publishing API: 1) Create container with video_url (upload to FB first) ou 2) Reels API
        try:
            import requests
            # Passo 1: upload do vídeo para Facebook e obter video_id; depois criar container Reels no Instagram
            page_token = os.getenv("INSTAGRAM_PAGE_ACCESS_TOKEN") or self._access_token
            ig_user_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
            if not ig_user_id:
                return None
            # Upload para Facebook Graph: POST /{page-id}/videos
            with open(video_path, "rb") as f:
                r = requests.post(
                    f"https://graph.facebook.com/v18.0/{ig_user_id}/video_reels",
                    params={"access_token": page_token},
                    data={"caption": description or f"{content_name} | {channel_label}", "share_to_feed": "true"},
                    files={"video_file": (Path(video_path).name, f, "video/mp4")},
                    timeout=300,
                )
            if r.ok:
                j = r.json()
                return {"id": j.get("id"), "url": j.get("permalink"), "platform": "instagram"}
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning("Instagram Reels upload (API may vary): %s", e)
        return None
