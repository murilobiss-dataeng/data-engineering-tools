"""
Kwai Publisher - Upload de vídeos para Kwai.

Requer credenciais da Kwai Open Platform.
Documentação: https://open.kwai.com/
Variáveis de ambiente: KWAI_APP_ID, KWAI_APP_SECRET, KWAI_ACCESS_TOKEN (ou OAuth)
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List

from .base import BasePublisher


class KwaiPublisher(BasePublisher):
    """Upload de vídeos para Kwai (Kwai / Kwai for Business)."""

    id = "kwai"
    name = "Kwai"

    def __init__(self):
        self._app_id = os.getenv("KWAI_APP_ID")
        self._app_secret = os.getenv("KWAI_APP_SECRET")
        self._access_token = os.getenv("KWAI_ACCESS_TOKEN")

    @property
    def is_configured(self) -> bool:
        return bool(self._app_id and (self._app_secret or self._access_token))

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
        # Kwai Open API: upload de vídeo via API de conteúdo
        # Implementação completa requer: POST para endpoint de upload, multipart, token
        try:
            import requests
            upload_url = os.getenv("KWAI_UPLOAD_URL", "https://open.kwai.com/api/upload")
            headers = {"Authorization": f"Bearer {self._access_token}"} if self._access_token else {}
            with open(video_path, "rb") as f:
                files = {"video": (Path(video_path).name, f, "video/mp4")}
                data = {"title": title[:100], "description": (description or f"{content_name} | {channel_label}")[:500]}
                r = requests.post(upload_url, headers=headers, data=data, files=files, timeout=300)
            if r.ok:
                j = r.json()
                video_id = j.get("data", {}).get("video_id") or j.get("video_id")
                return {"id": video_id, "url": j.get("data", {}).get("url") or f"https://www.kwai.com/video/{video_id}", "platform": "kwai"}
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning("Kwai upload (stub/API may vary): %s", e)
        return None
