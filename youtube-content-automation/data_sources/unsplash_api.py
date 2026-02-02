"""Unsplash API - Imagens profissionais gratuitas."""

import os
import random
import hashlib
import requests
from typing import Optional, Tuple
from io import BytesIO


class UnsplashAPI:
    """Busca imagens de alta qualidade no Unsplash."""

    BASE_URL = "https://api.unsplash.com"

    def __init__(self, access_key: Optional[str] = None):
        self.access_key = access_key or os.getenv("UNSPLASH_ACCESS_KEY")

    def search_photo(
        self,
        query: str,
        orientation: str = "landscape",
        size: Tuple[int, int] = (1920, 1080),
        output_dir: str = "outputs"
    ) -> Optional[str]:
        """
        Busca uma foto por palavra-chave e salva localmente.
        Retorna path da imagem ou None se falhar.
        """
        if not self.access_key:
            return None
        try:
            r = requests.get(
                f"{self.BASE_URL}/search/photos",
                params={
                    "query": query,
                    "orientation": orientation,
                    "per_page": 10,
                    "client_id": self.access_key
                },
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
            results = data.get("results", [])
            if not results:
                return None
            photo = random.choice(results)
            urls = photo.get("urls", {})
            # Pegar tamanho adequado
            img_url = urls.get("regular") or urls.get("full") or urls.get("raw")
            if not img_url:
                return None
            img_r = requests.get(img_url, timeout=15)
            img_r.raise_for_status()
            from PIL import Image
            img = Image.open(BytesIO(img_r.content))
            if img.mode != "RGB":
                img = img.convert("RGB")
            img = img.resize(size, Image.Resampling.LANCZOS)
            os.makedirs(output_dir, exist_ok=True)
            out_path = os.path.join(output_dir, f"unsplash_{hashlib.md5(query.encode()).hexdigest()[:12]}.jpg")
            img.save(out_path, "JPEG", quality=92)
            return out_path
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Unsplash search failed: {e}")
            return None
