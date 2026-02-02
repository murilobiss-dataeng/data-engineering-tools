"""
Facebook Publisher - Upload de Reels para Facebook (Meta Graph API).

Requer: App Facebook Developer, Page com permissão de vídeo.
Documentação: https://developers.facebook.com/docs/video-api
Variáveis de ambiente: META_APP_ID, META_APP_SECRET, FACEBOOK_PAGE_ACCESS_TOKEN, FACEBOOK_PAGE_ID
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List

from .base import BasePublisher


class FacebookPublisher(BasePublisher):
    """Upload de Reels/Vídeos para Facebook."""

    id = "facebook"
    name = "Facebook"

    def __init__(self):
        self._page_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN") or os.getenv("META_PAGE_ACCESS_TOKEN")
        self._page_id = os.getenv("FACEBOOK_PAGE_ID")

    @property
    def is_configured(self) -> bool:
        return bool(self._page_token and self._page_id)

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
        try:
            import requests
            url = f"https://graph-video.facebook.com/v18.0/{self._page_id}/videos"
            with open(video_path, "rb") as f:
                r = requests.post(
                    url,
                    params={"access_token": self._page_token},
                    data={"description": description or f"{content_name} | {channel_label}"},
                    files={"file": (Path(video_path).name, f, "video/mp4")},
                    timeout=600,
                )
            if r.ok:
                j = r.json()
                vid = j.get("id")
                return {"id": vid, "url": f"https://www.facebook.com/watch/?v={vid}", "platform": "facebook"}
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning("Facebook video upload: %s", e)
        return None
