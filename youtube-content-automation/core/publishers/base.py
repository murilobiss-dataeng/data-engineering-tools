"""
Base class for all publish destinations (YouTube, Twitter, Kwai, etc.).
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class BasePublisher(ABC):
    """Interface comum para publicar vídeo em uma plataforma."""

    id: str = ""
    name: str = ""

    @property
    @abstractmethod
    def is_configured(self) -> bool:
        """Retorna True se as credenciais/API estão configuradas."""
        pass

    @abstractmethod
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
        """
        Publica o vídeo na plataforma.

        Args:
            video_path: Caminho do arquivo de vídeo
            title: Título do vídeo/post
            description: Descrição (pode ser truncada por plataforma)
            content_name: Nome do conteúdo (ex: "Salmo 23", "João 3:16")
            channel_label: Rótulo do canal (ex: "Salmo do Dia")
            tags: Lista de tags/hashtags
            **kwargs: Argumentos específicos da plataforma

        Returns:
            Dict com url, id e outros dados do post, ou None se falhar
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id!r} configured={self.is_configured}>"
