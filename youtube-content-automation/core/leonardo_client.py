"""Cliente Leonardo AI para geração de cenas cinematográficas."""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)

API_BASE = "https://cloud.leonardo.ai/api/rest/v1"
PHOENIX_MODEL_ID = "de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3"


class LeonardoClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = (api_key or os.getenv("LEONARDO_API_KEY") or "").strip()
        if not self.api_key:
            raise RuntimeError("LEONARDO_API_KEY não configurada")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "accept": "application/json",
            "content-type": "application/json",
        }

    def create_generation(
        self,
        prompt: str,
        *,
        width: int = 1472,
        height: int = 832,
        seed: Optional[int] = None,
        num_images: int = 1,
        alchemy: bool = False,
        contrast: float = 3.5,
    ) -> str:
        payload = {
            "modelId": PHOENIX_MODEL_ID,
            "prompt": prompt[:1900],
            "num_images": num_images,
            "width": width,
            "height": height,
            "alchemy": alchemy,
            "contrast": contrast,
            "enhancePrompt": False,
        }
        if seed is not None:
            payload["seed"] = int(seed)
        r = requests.post(
            f"{API_BASE}/generations",
            headers=self.headers,
            json=payload,
            timeout=90,
        )
        if r.status_code >= 400:
            raise RuntimeError(f"Leonardo create failed: {r.status_code} {r.text[:500]}")
        data = r.json()
        gid = (data.get("sdGenerationJob") or {}).get("generationId")
        if not gid:
            raise RuntimeError(f"Leonardo sem generationId: {data}")
        return gid

    def wait_for_images(self, generation_id: str, timeout_sec: int = 180) -> list:
        deadline = time.time() + timeout_sec
        while time.time() < deadline:
            r = requests.get(
                f"{API_BASE}/generations/{generation_id}",
                headers=self.headers,
                timeout=45,
            )
            r.raise_for_status()
            gens = r.json().get("generations_by_pk") or {}
            status = gens.get("status")
            images = gens.get("generated_images") or []
            if status == "COMPLETE" and images:
                return images
            if status == "FAILED":
                raise RuntimeError(f"Leonardo generation FAILED: {gens}")
            time.sleep(3)
        raise TimeoutError(f"Leonardo timeout: {generation_id}")

    def generate_to_file(
        self,
        prompt: str,
        output_path: str,
        *,
        width: int = 1472,
        height: int = 832,
        seed: Optional[int] = None,
    ) -> str:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists() and out.stat().st_size > 10_000:
            logger.info("Reusando imagem existente: %s", out.name)
            return str(out)

        logger.info("Gerando cena Leonardo → %s", out.name)
        gid = self.create_generation(prompt, width=width, height=height, seed=seed)
        images = self.wait_for_images(gid)
        url = images[0]["url"]
        img = requests.get(url, timeout=120)
        img.raise_for_status()
        out.write_bytes(img.content)
        logger.info("Salvo: %s (%d bytes)", out, len(img.content))
        return str(out)
