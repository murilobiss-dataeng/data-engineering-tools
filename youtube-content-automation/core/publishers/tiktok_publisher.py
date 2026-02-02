"""
TikTok Publisher - Upload de vídeos para TikTok (Content Posting API).

Requer: TikTok for Developers app, OAuth 2.0.
Documentação: https://developers.tiktok.com/doc/content-posting-api-get-started
Variáveis de ambiente: TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_ACCESS_TOKEN
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List

from .base import BasePublisher


class TikTokPublisher(BasePublisher):
    """Upload de vídeos para TikTok."""

    id = "tiktok"
    name = "TikTok"

    def __init__(self):
        self._client_key = os.getenv("TIKTOK_CLIENT_KEY")
        self._client_secret = os.getenv("TIKTOK_CLIENT_SECRET")
        self._access_token = os.getenv("TIKTOK_ACCESS_TOKEN")

    @property
    def is_configured(self) -> bool:
        return bool(self._client_key and self._access_token)

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
            # TikTok Content Posting API: init upload -> upload bytes -> publish
            init_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
            headers = {"Authorization": f"Bearer {self._access_token}", "Content-Type": "application/json"}
            video_size = Path(video_path).stat().st_size
            payload = {
                "post_info": {"title": title[:150], "privacy_level": "PUBLIC_TO_EVERYONE"},
                "source_info": {"source": "PULL_FROM_URL", "size": video_size},
            }
            r = requests.post(init_url, headers=headers, json=payload, timeout=30)
            if not r.ok:
                return None
            j = r.json()
            publish_id = j.get("data", {}).get("publish_id")
            upload_url = j.get("data", {}).get("upload_url")
            if not upload_url:
                return None
            with open(video_path, "rb") as f:
                ru = requests.put(upload_url, data=f, headers={"Content-Type": "video/mp4"}, timeout=300)
            if ru.ok and publish_id:
                return {"id": publish_id, "url": f"https://www.tiktok.com/@{os.getenv('TIKTOK_USERNAME', '')}/video/{publish_id}", "platform": "tiktok"}
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning("TikTok upload (API flow may vary): %s", e)
        return None
