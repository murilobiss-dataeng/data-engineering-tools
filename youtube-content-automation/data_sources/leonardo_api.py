"""Leonardo.ai API - Geração de imagens por IA."""

import os
import time
import logging
import requests
from typing import Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

LEONARDO_API_URL = "https://cloud.leonardo.ai/api/rest/v1"
# Modelo padrão - Leonardo Diffusion XL
DEFAULT_MODEL_ID = "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3"
# Dimensões suportadas - usar 1024x576 para 16:9
SUPPORTED_SIZES = [(1024, 576), (1344, 768), (1216, 832), (1152, 896), (896, 1152)]


class LeonardoAPI:
    """Cliente para API Leonardo.ai."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("LEONARDO_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _closest_size(self, width: int, height: int) -> Tuple[int, int]:
        """Retorna o tamanho mais próximo suportado (aspect ratio 16:9)."""
        for w, h in SUPPORTED_SIZES:
            if w >= width and h >= height:
                return (w, h)
        return SUPPORTED_SIZES[0]

    def generate_image(
        self,
        prompt: str,
        size: Tuple[int, int] = (1024, 576),
        negative_prompt: Optional[str] = None,
        model_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Gera imagem e retorna o generationId.
        """
        if not self.api_key:
            logger.warning("LEONARDO_API_KEY não configurada")
            return None

        w, h = self._closest_size(size[0], size[1])
        payload = {
            "prompt": prompt,
            "modelId": model_id or DEFAULT_MODEL_ID,
            "width": w,
            "height": h,
            "num_images": 1,
        }
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt

        try:
            r = requests.post(
                f"{LEONARDO_API_URL}/generations",
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            r.raise_for_status()
            data = r.json()
            gen_id = data.get("sdGenerationJob", {}).get("generationId")
            return gen_id
        except Exception as e:
            logger.warning(f"Leonardo API error: {e}")
            return None

    def get_generation(self, generation_id: str) -> Optional[dict]:
        """Obtém resultado da geração (polling)."""
        if not self.api_key:
            return None
        try:
            r = requests.get(
                f"{LEONARDO_API_URL}/generations/{generation_id}",
                headers=self.headers,
                timeout=15,
            )
            r.raise_for_status()
            return r.json()
        except Exception as e:
            logger.debug(f"Leonardo get generation: {e}")
            return None

    def wait_and_download(
        self,
        generation_id: str,
        output_path: str,
        max_wait: int = 120,
        poll_interval: int = 5,
    ) -> Optional[str]:
        """
        Aguarda geração concluir, baixa imagem e salva.
        Retorna path do arquivo ou None.
        """
        start = time.time()
        while (time.time() - start) < max_wait:
            data = self.get_generation(generation_id)
            if not data:
                time.sleep(poll_interval)
                continue

            gen = data.get("generations_by_pk", {})
            status = gen.get("status")
            if status == "FAILED":
                logger.warning("Leonardo generation failed")
                return None
            if status == "COMPLETE":
                images = gen.get("generated_images", []) or []
                if images and images[0].get("url"):
                    url = images[0]["url"]
                    try:
                        r = requests.get(url, timeout=30)
                        r.raise_for_status()
                        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                        with open(output_path, "wb") as f:
                            f.write(r.content)
                        return output_path
                    except Exception as e:
                        logger.warning(f"Leonardo download failed: {e}")
                        return None

            time.sleep(poll_interval)
        logger.warning("Leonardo generation timeout")
        return None

    def generate_and_save(
        self,
        prompt: str,
        output_path: str,
        size: Tuple[int, int] = (1024, 576),
        negative_prompt: str = "blurry, low quality, distorted, watermark, text",
    ) -> Optional[str]:
        """
        Fluxo completo: gera, aguarda e salva.
        """
        gen_id = self.generate_image(prompt, size, negative_prompt)
        if not gen_id:
            return None
        return self.wait_and_download(gen_id, output_path)
