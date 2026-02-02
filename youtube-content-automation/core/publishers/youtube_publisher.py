"""
YouTube Publisher - Upload de Shorts para YouTube via Data API v3.

Requer: google-api-python-client, google-auth-oauthlib
Configuração: client_secrets.json (OAuth 2.0) em config/ ou via GOOGLE_CLIENT_SECRETS_PATH
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List

from .base import BasePublisher


class YouTubePublisher(BasePublisher):
    """Upload de vídeos (Shorts) para YouTube."""

    id = "youtube"
    name = "YouTube"

    def __init__(self):
        self._youtube = None
        self._credentials = None

    @property
    def is_configured(self) -> bool:
        try:
            secrets_path = os.getenv("GOOGLE_CLIENT_SECRETS_PATH") or self._find_client_secrets()
            return bool(secrets_path and Path(secrets_path).exists())
        except Exception:
            return False

    def _find_client_secrets(self) -> Optional[str]:
        base = Path(__file__).resolve().parents[2]
        for p in (base / "config" / "client_secrets.json", base / "client_secrets.json"):
            if p.exists():
                return str(p)
        return None

    def _get_youtube(self):
        if self._youtube is None:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload

            scopes = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]
            secrets_path = os.getenv("GOOGLE_CLIENT_SECRETS_PATH") or self._find_client_secrets()
            if not secrets_path:
                raise RuntimeError("YouTube: client_secrets.json não encontrado. Coloque em config/client_secrets.json ou defina GOOGLE_CLIENT_SECRETS_PATH")

            creds = None
            token_path = Path(__file__).resolve().parents[2] / "config" / "youtube_token.json"
            if token_path.exists():
                creds = Credentials.from_authorized_user_file(str(token_path), scopes)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(secrets_path, scopes)
                    creds = flow.run_local_server(port=0)
                token_path.parent.mkdir(parents=True, exist_ok=True)
                with open(token_path, "w") as f:
                    f.write(creds.to_json())
            self._youtube = build("youtube", "v3", credentials=creds)
        return self._youtube

    def publish(
        self,
        video_path: str,
        title: str,
        description: str = "",
        content_name: str = "",
        channel_label: str = "Salmo do Dia",
        tags: Optional[List[str]] = None,
        privacy: str = "public",
        **kwargs: Any,
    ) -> Optional[Dict[str, Any]]:
        try:
            from googleapiclient.http import MediaFileUpload
        except ImportError:
            raise ImportError("YouTube upload requer: pip install google-api-python-client google-auth-oauthlib")

        video_path = Path(video_path)
        if not video_path.exists():
            return None

        try:
            body = {
                "snippet": {
                    "title": title[:100],
                    "description": description or f"{content_name} | {channel_label}",
                    "tags": (tags or [])[:500],
                    "categoryId": "22",
                },
                "status": {
                    "privacyStatus": privacy,
                    "selfDeclaredMadeForKids": False,
                },
            }
            insert_request = self._get_youtube().videos().insert(
                part="snippet,status",
                body=body,
                media_body=MediaFileUpload(
                    str(video_path), mimetype="video/mp4", resumable=True, chunksize=1024 * 1024
                ),
            )
            response = insert_request.execute()
            video_id = response.get("id")
            return {
                "id": video_id,
                "url": f"https://www.youtube.com/shorts/{video_id}" if video_id else None,
                "platform": "youtube",
            }
        except Exception as e:
            import logging
            logging.getLogger(__name__).exception("YouTube upload failed: %s", e)
            return None
