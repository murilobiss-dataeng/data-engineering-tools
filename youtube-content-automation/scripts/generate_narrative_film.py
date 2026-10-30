#!/usr/bin/env python3
"""Gera o filme narrativo cinematográfico do Salmo 23 (≥ 2 minutos)."""

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from dotenv import load_dotenv

load_dotenv(os.path.join(ROOT, ".env"))


def main():
    parser = argparse.ArgumentParser(description="Filme narrativo Salmo 23")
    parser.add_argument("--output", "-o", default=None, help="Pasta de saída")
    parser.add_argument("--skip-images", action="store_true", help="Reusa cenas já geradas")
    args = parser.parse_args()

    from core.narrative_salmo_pipeline import run_narrative_salmo23_pipeline

    result = run_narrative_salmo23_pipeline(output_dir=args.output, skip_images=args.skip_images)
    print("\n" + "=" * 60)
    print("FILME PRONTO")
    print(f"  Salmo: {result.get('psalm')}")
    print(f"  Duração: {result.get('duration_seconds'):.1f}s")
    print(f"  Vídeo: {result.get('video_path')}")
    print(f"  Pasta: {result.get('output_dir')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
