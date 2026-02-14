"""
Dispatcher - Publica vídeo em múltiplos destinos (YouTube, Twitter, Kwai, IG, etc.).
"""

import os
import logging
from typing import Dict, Any, List, Optional

from .base import BasePublisher
from .youtube_publisher import YouTubePublisher
from .twitter_publisher import TwitterPublisherAdapter
from .kwai_publisher import KwaiPublisher
from .instagram_publisher import InstagramPublisher
from .tiktok_publisher import TikTokPublisher
from .facebook_publisher import FacebookPublisher
from .linkedin_publisher import LinkedInPublisher
from .pinterest_publisher import PinterestPublisher

logger = logging.getLogger(__name__)

# Registro de todos os destinos (uma instância por plataforma; aliases apontam para a mesma)
_youtube = YouTubePublisher()
_twitter = TwitterPublisherAdapter()
_kwai = KwaiPublisher()
_instagram = InstagramPublisher()
_tiktok = TikTokPublisher()
_facebook = FacebookPublisher()
_linkedin = LinkedInPublisher()
_pinterest = PinterestPublisher()

DESTINATIONS: Dict[str, BasePublisher] = {
    "youtube": _youtube,
    "twitter": _twitter,
    "kwai": _kwai,
    "instagram": _instagram,
    "ig": _instagram,
    "tiktok": _tiktok,
    "facebook": _facebook,
    "fb": _facebook,
    "linkedin": _linkedin,
    "pinterest": _pinterest,
    "pin": _pinterest,
}

# Nomes amigáveis para exibição
DESTINATION_NAMES = {
    "youtube": "YouTube",
    "twitter": "Twitter/X",
    "kwai": "Kwai",
    "instagram": "Instagram",
    "ig": "Instagram",
    "tiktok": "TikTok",
    "facebook": "Facebook",
    "fb": "Facebook",
    "linkedin": "LinkedIn",
    "pinterest": "Pinterest",
    "pin": "Pinterest",
}


def get_available_destinations() -> List[str]:
    """Retorna lista de IDs de destinos disponíveis (sem aliases duplicados)."""
    seen = set()
    out = []
    for d in ("youtube", "twitter", "kwai", "instagram", "tiktok", "facebook", "linkedin", "pinterest"):
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out


def get_configured_destinations() -> List[str]:
    """Retorna apenas destinos que estão configurados (credenciais presentes)."""
    return [d for d in get_available_destinations() if DESTINATIONS[d].is_configured]


def parse_destinations(value: Optional[str]) -> List[str]:
    """
    Interpreta --publish-to ou PUBLISH_TO.
    Ex.: "youtube,twitter,kwai,ig" -> ["youtube", "twitter", "kwai", "instagram"]
    "all" -> todos os configurados (ou todos disponíveis).
    """
    if not value or not value.strip():
        return get_configured_destinations() or get_available_destinations()
    value = value.strip().lower()
    if value == "all":
        return get_configured_destinations() or get_available_destinations()
    raw = [x.strip().lower() for x in value.split(",") if x.strip()]
    out = []
    for r in raw:
        if r in DESTINATIONS:
            pub = DESTINATIONS[r]
            key = pub.id
            if key not in out:
                out.append(key)
        else:
            logger.warning("Destino desconhecido ignorado: %s", r)
    return out


def publish_to_destinations(
    video_path: str,
    title: str,
    description: str = "",
    content_name: str = "",
    channel_label: str = "Salmo do Dia",
    tags: Optional[List[str]] = None,
    destinations: Optional[List[str]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Publica o vídeo em todos os destinos solicitados.

    Args:
        video_path: Caminho do vídeo
        title: Título
        description: Descrição
        content_name: Nome do conteúdo (ex: Salmo 23, João 3:16)
        channel_label: Rótulo do canal
        tags: Lista de tags (se vazio, YouTube pode gerar por título+tema via kwargs theme/tema)
        destinations: Lista de IDs (youtube, twitter, kwai, instagram, tiktok, facebook, linkedin).
                      Se None, usa PUBLISH_TO ou todos configurados.
        kwargs: content_hash + channel_namespace → bloqueio anti-repost (cancela se hash já publicado).
                description_with_chapters, duration_estimate_sec, theme, publish_at, etc. para YouTube.

    Returns:
        Dict com chave por plataforma: {"youtube": {...}, "twitter": {...}, ...}
    """
    if destinations is None:
        destinations = parse_destinations(os.getenv("PUBLISH_TO"))

    # Bloqueio de repostagem: se content_hash + channel_namespace, verificar antes de publicar
    content_hash_val = kwargs.get("content_hash")
    channel_namespace = kwargs.get("channel_namespace")
    if content_hash_val and channel_namespace:
        try:
            from core.publication_options import ContentHashStorage
            storage = ContentHashStorage(channel_namespace, base_dir=kwargs.get("output_base_dir", "outputs"))
            if storage.is_duplicate(content_hash_val):
                logger.warning("Upload cancelado: conteúdo já publicado (hash duplicado).")
                return {dest_id: {"cancelled": True, "reason": "duplicate_content_hash"} for dest_id in destinations}
        except Exception as e:
            logger.exception("Erro ao verificar hash anti-repost: %s", e)

    results: Dict[str, Any] = {}
    for dest_id in destinations:
        pub = DESTINATIONS.get(dest_id)
        if not pub:
            continue
        if not pub.is_configured:
            logger.warning("%s: não configurado, pulando.", pub.name)
            results[dest_id] = {"ok": False, "error": "not_configured"}
            continue
        try:
            r = pub.publish(
                video_path=video_path,
                title=title,
                description=description,
                content_name=content_name,
                channel_label=channel_label,
                tags=tags,
                **kwargs,
            )
            results[dest_id] = r if r is not None else {"ok": False, "error": "upload_failed"}
            # Após sucesso: salvar hash para impedir repostagem futura
            if content_hash_val and channel_namespace and results[dest_id] and isinstance(results[dest_id], dict) and results[dest_id].get("id"):
                try:
                    from core.publication_options import ContentHashStorage
                    storage = ContentHashStorage(channel_namespace, base_dir=kwargs.get("output_base_dir", "outputs"))
                    storage.save_hash(content_hash_val)
                except Exception as e:
                    logger.exception("Erro ao salvar hash após publicação: %s", e)
        except Exception as e:
            logger.exception("Erro ao publicar em %s: %s", dest_id, e)
            results[dest_id] = {"ok": False, "error": str(e)}
    return results
