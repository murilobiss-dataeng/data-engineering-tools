"""
LinkedIn Publisher - Upload de vídeos para LinkedIn (Share API).

Requer: App LinkedIn Developer, r_liteprofile + w_member_social ou r_organization_social.
Documentação: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/share-api
Variáveis de ambiente: LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_ACCESS_TOKEN
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List

from .base import BasePublisher


class LinkedInPublisher(BasePublisher):
    """Publica vídeo no LinkedIn (compartilhamento com mídia)."""

    id = "linkedin"
    name = "LinkedIn"

    def __init__(self):
        self._client_id = os.getenv("LINKEDIN_CLIENT_ID")
        self._client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
        self._access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")

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
        # LinkedIn: registro de upload de vídeo + UGC Post com referência ao vídeo
        try:
            import requests
            headers = {"Authorization": f"Bearer {self._access_token}", "X-Restli-Protocol-Version": "2.0.0"}
            # Inicializar upload
            init_url = "https://api.linkedin.com/rest/videos?action=initializeUpload"
            size = Path(video_path).stat().st_size
            payload = {"initializeUploadRequest": {"owner": f"urn:li:person:{os.getenv('LINKEDIN_PERSON_URN', '')}", "fileSizeBytes": size, "uploadCaptions": False}}
            r = requests.post(init_url, headers=headers, json=payload, timeout=30)
            if not r.ok:
                return None
            j = r.json()
            upload_url = j.get("value", {}).get("uploadInstructions", [{}])[0].get("uploadUrl")
            if not upload_url:
                return None
            with open(video_path, "rb") as f:
                ru = requests.put(upload_url, data=f, headers={"Content-Type": "video/mp4"}, timeout=300)
            if ru.ok:
                video_urn = j.get("value", {}).get("video")
                return {"id": video_urn, "url": None, "platform": "linkedin"}
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning("LinkedIn video upload: %s", e)
        return None
