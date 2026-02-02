#!/usr/bin/env python3
"""Script para testar upload de vídeo Salmo do Dia já gerado."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / 'config' / 'api_keys.env')

from main import upload_video

outputs = PROJECT_ROOT / 'outputs'
salmo_shorts = sorted(outputs.glob('salmo_short_*.mp4'), key=lambda p: p.stat().st_mtime, reverse=True)
salmo_longs = sorted(outputs.glob('salmo_long_*.mp4'), key=lambda p: p.stat().st_mtime, reverse=True)

if not salmo_shorts and not salmo_longs:
    print("Nenhum vídeo salmo encontrado em outputs/")
    sys.exit(1)

# Upload short (menor, mais rápido)
video_path = str(salmo_shorts[0]) if salmo_shorts else str(salmo_longs[0])
result = {
    'video_path': video_path,
    'title': 'Salmo 23 | Salmo do Dia | Shorts',
    'description': '📖 Salmo 23\n\nO Senhor é meu pastor; nada me faltará.\n\n#palavra #reflexão #fé',
    'tags': ['salmo', 'bíblia', 'reflexão', 'palavra', 'fé', 'salmo 23']
}

print(f"Uploadando: {video_path}")
upload_video(result, channel_name='salmo_dia')
