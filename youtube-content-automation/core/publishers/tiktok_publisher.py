"""
TikTok Publisher - Upload de vídeos para TikTok (Content Posting API).

Requer: TikTok for Developers app, OAuth 2.0, scope video.publish (ou video.upload para inbox).
Documentação: https://developers.tiktok.com/doc/content-posting-api-get-started-upload-content
Variáveis de ambiente: TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_ACCESS_TOKEN
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

from .base import BasePublisher

logger = logging.getLogger(__name__)


class TikTokPublisher(BasePublisher):
    """Upload de vídeos para TikTok via FILE_UPLOAD (envio do arquivo local)."""

    id = "tiktok"
    name = "TikTok"

    def __init__(self):
        self._client_key = (os.getenv("TIKTOK_CLIENT_KEY") or "").strip()
        self._client_secret = (os.getenv("TIKTOK_CLIENT_SECRET") or "").strip()
        self._access_token = (os.getenv("TIKTOK_ACCESS_TOKEN") or "").strip()

    @property
    def is_configured(self) -> bool:
        return bool(self._client_key and self._client_secret)

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
            return {"ok": False, "error": "TikTok não configurado (TIKTOK_CLIENT_KEY/SECRET)"}
        if not self._access_token:
            logger.warning(
                "TikTok: TIKTOK_ACCESS_TOKEN não definido. Obtenha via OAuth 2.0 no TikTok for Developers."
            )
            return {"ok": False, "error": "TIKTOK_ACCESS_TOKEN não configurado (obtenha via OAuth 2.0)"}
        try:
            import requests
            video_path = Path(video_path)
            if not video_path.exists():
                return {"ok": False, "error": f"Vídeo não encontrado: {video_path}"}
            video_size = video_path.stat().st_size

            # 1) Init: FILE_UPLOAD (envio local). Inbox = rascunho na caixa do usuário para publicar no app.
            init_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
            headers = {
                "Authorization": f"Bearer {self._access_token}",
                "Content-Type": "application/json; charset=UTF-8",
            }
            # Um único chunk = arquivo inteiro (TikTok aceita até ~4GB; shorts cabem em 1 chunk)
            chunk_size = video_size
            total_chunk_count = 1
            payload = {
                "post_info": {
                    "title": (title or "Salmo do Dia")[:2200],
                    "privacy_level": "PUBLIC_TO_EVERYONE",
                },
                "source_info": {
                    "source": "FILE_UPLOAD",
                    "video_size": video_size,
                    "chunk_size": chunk_size,
                    "total_chunk_count": total_chunk_count,
                },
            }
            logger.info("TikTok init: POST %s (video_size=%s, chunks=%s)", init_url, video_size, total_chunk_count)
            r = requests.post(init_url, headers=headers, json=payload, timeout=30)
            body = r.json() if r.text else {}
            err = body.get("error", {})
            code = err.get("code", "")
            msg = err.get("message", "")

            if not r.ok:
                logger.warning("TikTok init HTTP %s: %s", r.status_code, body)
                return {"ok": False, "error": f"TikTok init {r.status_code}: {code or r.reason} - {msg or r.text}"}
            if code and code != "ok":
                logger.warning("TikTok init error: code=%s message=%s", code, msg)
                return {"ok": False, "error": f"TikTok: {code} - {msg}"}

            data = body.get("data", {})
            publish_id = data.get("publish_id")
            upload_url = data.get("upload_url")
            if not upload_url or not publish_id:
                logger.warning("TikTok init sem upload_url/publish_id: %s", data)
                return {"ok": False, "error": "TikTok não retornou upload_url ou publish_id"}

            # 2) PUT do vídeo (um único chunk se o arquivo for menor que chunk_size)
            with open(video_path, "rb") as f:
                content = f.read()
            put_headers = {
                "Content-Type": "video/mp4",
                "Content-Length": str(len(content)),
                "Content-Range": f"bytes 0-{len(content) - 1}/{video_size}",
            }
            logger.info("TikTok upload: PUT %s (Content-Length=%s)", upload_url[:80], len(content))
            ru = requests.put(upload_url, data=content, headers=put_headers, timeout=300)
            if not ru.ok:
                logger.warning("TikTok PUT HTTP %s: %s", ru.status_code, ru.text[:500])
                return {"ok": False, "error": f"TikTok upload PUT {ru.status_code}: {ru.text[:200]}"}

            username = os.getenv("TIKTOK_USERNAME", "")
            url = f"https://www.tiktok.com/@{username}/video/{publish_id}" if username else f"https://www.tiktok.com (publish_id={publish_id})"
            logger.info("TikTok: vídeo enviado para inbox. publish_id=%s", publish_id)
            return {"id": publish_id, "url": url, "platform": "tiktok", "ok": True}
        except Exception as e:
            logger.exception("TikTok upload falhou: %s", e)
            return {"ok": False, "error": str(e)}
