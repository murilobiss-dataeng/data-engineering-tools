"""
Twitter/X Publisher - Wrapper para o publisher existente em core.twitter_publisher.
"""

from typing import Optional, Dict, Any, List

from .base import BasePublisher


class TwitterPublisherAdapter(BasePublisher):
    """Publica vídeos no Twitter/X (Shorts)."""

    id = "twitter"
    name = "Twitter/X"

    def __init__(self):
        self._publisher = None

    def _get_publisher(self):
        if self._publisher is None:
            from core.twitter_publisher import TwitterPublisher
            self._publisher = TwitterPublisher()
        return self._publisher

    @property
    def is_configured(self) -> bool:
        return self._get_publisher().is_configured

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
        pub = self._get_publisher()
        return pub.post_psalm(
            video_path,
            content_name or title,
            description=description or None,
            channel_label=channel_label,
        )
