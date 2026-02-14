"""
YouTube Publisher - Upload de Shorts para YouTube via Data API v3.

Opções de publicação:
- Tags automáticas (título + tema) via kwargs theme/title ou tags.
- Capítulos/key moments: passar description_with_chapters ou duration_estimate_sec para gerar.
- embeddable=True, publicStatsViewable=True (incorporação e feed).
- publish_at (RFC 3339): agenda publicação (privacy=private até o horário).
- Comentários/moderação: definidos no YouTube Studio por canal (API não altera no insert).
- Dublagem automática: desativar no Studio. Remix: ativar no Studio se desejado.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List

from .base import BasePublisher
from core.publication_options import generate_tags_from_title_and_theme, build_description_with_chapters


class YouTubePublisher(BasePublisher):
    """Upload de vídeos (Shorts) para YouTube. Usa canal (channel_namespace/CONTENT_CHANNEL_ID) para token e category_id."""

    id = "youtube"
    name = "YouTube"

    def __init__(self):
        self._youtube_by_channel: Dict[str, Any] = {}  # channel_key -> youtube client

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

    def _get_token_path_for_channel(self, channel_name: Optional[str]) -> Path:
        """Token OAuth por canal: config/<canal>/youtube_token.json ou youtube_channels.yaml credentials_path."""
        base = Path(__file__).resolve().parents[2]
        default_token = base / "config" / "youtube_token.json"
        if not channel_name or not channel_name.strip():
            return default_token
        try:
            import yaml
            config_path = base / "config" / "youtube_channels.yaml"
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f) or {}
                chan = (config.get("channels") or {}).get(channel_name.strip())
                if chan:
                    cred_path = chan.get("credentials_path")
                    if cred_path:
                        p = Path(cred_path)
                        if not p.is_absolute():
                            p = base / p
                        if p.is_dir():
                            p = p / "youtube_token.json"
                        return p
        except Exception:
            pass
        # Convenção: config/<canal>/youtube_token.json; salmo_do_dia aceita fallback salmo_dia
        name = channel_name.strip()
        per_channel = base / "config" / name / "youtube_token.json"
        if name == "salmo_do_dia" and not per_channel.exists():
            fallback = base / "config" / "salmo_dia" / "youtube_token.json"
            if fallback.exists():
                return fallback
        return per_channel

    def _get_youtube(self, channel_name: Optional[str] = None):
        """Cliente YouTube; usa token do canal quando configurado (evita enviar para dica_carreira_dia)."""
        key = (channel_name or "").strip() or "__default__"
        if key not in self._youtube_by_channel:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload

            scopes = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]
            secrets_path = os.getenv("GOOGLE_CLIENT_SECRETS_PATH") or self._find_client_secrets()
            if not secrets_path:
                raise RuntimeError("YouTube: client_secrets.json não encontrado. Coloque em config/client_secrets.json ou defina GOOGLE_CLIENT_SECRETS_PATH")

            token_path = self._get_token_path_for_channel(channel_name)
            creds = None
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
            self._youtube_by_channel[key] = build("youtube", "v3", credentials=creds)
        return self._youtube_by_channel[key]

    def _get_category_id_for_channel(self, channel_name: Optional[str]) -> str:
        """Category_id do canal em config/youtube_channels.yaml (ex.: salmo_dia -> 28)."""
        if not channel_name or not channel_name.strip():
            return "22"
        try:
            import yaml
            base = Path(__file__).resolve().parents[2]
            config_path = base / "config" / "youtube_channels.yaml"
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f) or {}
                chan = (config.get("channels") or {}).get(channel_name.strip())
                if chan and chan.get("category_id"):
                    return str(chan["category_id"])
        except Exception:
            pass
        return "22"

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

        # 1) Tags automáticas: título + tema; ou usar tags passadas
        if tags is None or len(tags) == 0:
            theme = kwargs.get("theme") or kwargs.get("tema") or content_name
            tags = generate_tags_from_title_and_theme(
                title=title,
                theme=theme,
                max_tags=30,
                extra_keywords=kwargs.get("extra_tags"),
            )
        tags = (tags or [])[:500]

        # 2) Capítulos/key moments: descrição com timestamps
        desc_final = kwargs.get("description_with_chapters") or description
        if not desc_final and kwargs.get("duration_estimate_sec") is not None:
            desc_final = build_description_with_chapters(
                description or f"{content_name} | {channel_label}",
                duration_estimate_sec=float(kwargs["duration_estimate_sec"]),
            )
        if not desc_final:
            desc_final = description or f"{content_name} | {channel_label}"

        # 3) Agendamento: publish_at (RFC 3339) → privacy private até o horário
        publish_at = kwargs.get("publish_at")
        if publish_at:
            privacy = "private"

        # 4) Status: incorporação ativa, estatísticas públicas (feed de inserções)
        # Comentários/moderação: configurados no YouTube Studio por canal
        # Dublagem automática: desativar no Studio. Remix: ativar no Studio
        status: Dict[str, Any] = {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
            "embeddable": True,
            "publicStatsViewable": True,
        }
        if publish_at:
            status["publishAt"] = publish_at

        # Canal: token e category_id por canal (evita upload ir para dica_carreira_dia)
        channel = kwargs.get("channel_namespace") or os.getenv("CONTENT_CHANNEL_ID") or None
        category_id = kwargs.get("category_id") or self._get_category_id_for_channel(channel) or "22"
        body = {
            "snippet": {
                "title": title[:100],
                "description": desc_final,
                "tags": tags,
                "categoryId": category_id,
            },
            "status": status,
        }

        try:
            insert_request = self._get_youtube(channel).videos().insert(
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
