"""Main entry point for YouTube content automation."""

import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Configs em config/ (relativo ao projeto)
PROJECT_ROOT = Path(__file__).parent.resolve()
load_dotenv(PROJECT_ROOT / 'config' / 'api_keys.env')

# Import channel processors
from channels.placar_dia.channel_processor import PlacarDiaProcessor
from channels.explicado_shorts.channel_processor import ExplicadoShortsProcessor
from channels.quanto_rende.channel_processor import QuantoRendeProcessor
from channels.series_explicadas.channel_processor import SeriesExplicadasProcessor
from channels.salmo_dia.channel_processor import SalmoDiaProcessor
from channels.receita_dia.channel_processor import ReceitaDiaProcessor
from channels.exercicio_dia.channel_processor import ExercicioDiaProcessor
from channels.motivacao_dia.channel_processor import MotivacaoDiaProcessor
from channels.curiosidade_dia.channel_processor import CuriosidadeDiaProcessor
from channels.dica_carreira_dia.channel_processor import DicaCarreiraDiaProcessor
from core.youtube_uploader import YouTubeUploader

CHANNELS = [
    'placar_dia', 'explicado_shorts', 'quanto_rende', 'series_explicadas',
    'salmo_dia', 'receita_dia', 'exercicio_dia', 'motivacao_dia',
    'curiosidade_dia', 'dica_carreira_dia'
]


def process_channel(channel_name: str, upload: bool = False):
    """Process a specific channel.
    
    Args:
        channel_name: Name of the channel to process
        upload: Whether to upload to YouTube
    """
    print(f"\n{'='*50}")
    print(f"Processando canal: {channel_name}")
    print(f"{'='*50}\n", flush=True)
    
    if channel_name == 'placar_dia':
        processor = PlacarDiaProcessor()
        results = processor.process_round()
        
        for result in results:
            print(f"Generated: {result.get('title', 'Unknown')}")
            if upload:
                # Upload long-form video
                if 'video_path' in result:
                    upload_video({
                        'video_path': result['video_path'],
                        'title': result['title'],
                        'description': result['description'],
                        'tags': result['tags']
                    }, channel_name='placar_dia')
                # Upload shorts video
                if 'short_video_path' in result:
                    short_title = result['title'].replace(' - Resumo Completo', ' - Shorts')
                    upload_video({
                        'video_path': result['short_video_path'],
                        'title': short_title,
                        'description': result['description'],
                        'tags': result['tags']
                    }, channel_name='placar_dia')
    
    elif channel_name == 'explicado_shorts':
        processor = ExplicadoShortsProcessor()
        result = processor.process_topic()
        print(f"Generated: {result.get('title', 'Unknown')}")
        if upload:
            # Upload long-form video
            if 'video_path' in result:
                upload_video({
                    'video_path': result['video_path'],
                    'title': result['title'],
                    'description': result['description'],
                    'tags': result['tags']
                }, channel_name='explicado_shorts')
            # Upload shorts video
            if 'short_video_path' in result:
                short_title = result['title'].replace(' | Explicado em Shorts', ' | Shorts')
                upload_video({
                    'video_path': result['short_video_path'],
                    'title': short_title,
                    'description': result['description'],
                    'tags': result['tags']
                }, channel_name='explicado_shorts')
    
    elif channel_name == 'quanto_rende':
        processor = QuantoRendeProcessor()
        result = processor.process_investment()
        print(f"Generated: {result.get('title', 'Unknown')}")
        if upload:
            # Upload long-form video
            if 'video_path' in result:
                upload_video({
                    'video_path': result['video_path'],
                    'title': result['title'],
                    'description': result['description'],
                    'tags': result['tags']
                }, channel_name='quanto_rende')
            # Upload shorts video
            if 'short_video_path' in result:
                short_title = result['title'].replace(' | Cálculo Completo', ' | Shorts')
                upload_video({
                    'video_path': result['short_video_path'],
                    'title': short_title,
                    'description': result['description'],
                    'tags': result['tags']
                }, channel_name='quanto_rende')
    
    elif channel_name == 'series_explicadas':
        processor = SeriesExplicadasProcessor()
        result = processor.process_series()
        print(f"Generated: {result.get('title', 'Unknown')}")
        if upload:
            if 'video_path' in result:
                upload_video({'video_path': result['video_path'], 'title': result['title'], 'description': result['description'], 'tags': result['tags']}, channel_name='series_explicadas')
            if 'short_video_path' in result:
                upload_video({'video_path': result['short_video_path'], 'title': result['title'].replace(' | Series Explicadas', ' | Shorts'), 'description': result['description'], 'tags': result['tags']}, channel_name='series_explicadas')
    elif channel_name == 'salmo_dia':
        processor = SalmoDiaProcessor()
        result = processor.process_salmo()
        print(f"\n✓ Conteúdo gerado: {result.get('title', 'Unknown')}\n", flush=True)
        if upload:
            if 'video_path' in result:
                print("  Fazendo upload do vídeo longo...", flush=True)
                upload_video({'video_path': result['video_path'], 'title': result['title'], 'description': result['description'], 'tags': result['tags']}, channel_name='salmo_dia')
            if 'short_video_path' in result:
                print("  Fazendo upload do short...", flush=True)
                upload_video({'video_path': result['short_video_path'], 'title': result['title'].replace(' | Salmo do Dia', ' | Shorts'), 'description': result['description'], 'tags': result['tags']}, channel_name='salmo_dia')
    elif channel_name == 'receita_dia':
        processor = ReceitaDiaProcessor()
        result = processor.process_receita()
        print(f"Generated: {result.get('title', 'Unknown')}")
        if upload:
            if 'video_path' in result:
                upload_video({'video_path': result['video_path'], 'title': result['title'], 'description': result['description'], 'tags': result['tags']}, channel_name='receita_dia')
            if 'short_video_path' in result:
                upload_video({'video_path': result['short_video_path'], 'title': result['title'].replace(' | Receita do Dia', ' | Shorts'), 'description': result['description'], 'tags': result['tags']}, channel_name='receita_dia')
    elif channel_name == 'exercicio_dia':
        processor = ExercicioDiaProcessor()
        result = processor.process_exercicio()
        print(f"Generated: {result.get('title', 'Unknown')}")
        if upload:
            if 'video_path' in result:
                upload_video({'video_path': result['video_path'], 'title': result['title'], 'description': result['description'], 'tags': result['tags']}, channel_name='exercicio_dia')
            if 'short_video_path' in result:
                upload_video({'video_path': result['short_video_path'], 'title': result['title'].replace(' | Exercício do Dia', ' | Shorts'), 'description': result['description'], 'tags': result['tags']}, channel_name='exercicio_dia')
    elif channel_name == 'motivacao_dia':
        processor = MotivacaoDiaProcessor()
        result = processor.process_motivacao()
        print(f"Generated: {result.get('title', 'Unknown')}")
        if upload:
            if 'video_path' in result:
                upload_video({'video_path': result['video_path'], 'title': result['title'], 'description': result['description'], 'tags': result['tags']}, channel_name='motivacao_dia')
            if 'short_video_path' in result:
                upload_video({'video_path': result['short_video_path'], 'title': result['title'].replace(' | Motivação do Dia', ' | Shorts'), 'description': result['description'], 'tags': result['tags']}, channel_name='motivacao_dia')
    elif channel_name == 'curiosidade_dia':
        processor = CuriosidadeDiaProcessor()
        result = processor.process_curiosidade()
        print(f"Generated: {result.get('title', 'Unknown')}")
        if upload:
            if 'video_path' in result:
                upload_video({'video_path': result['video_path'], 'title': result['title'], 'description': result['description'], 'tags': result['tags']}, channel_name='curiosidade_dia')
            if 'short_video_path' in result:
                upload_video({'video_path': result['short_video_path'], 'title': result['title'].replace(' | Curiosidade do Dia', ' | Shorts'), 'description': result['description'], 'tags': result['tags']}, channel_name='curiosidade_dia')
    elif channel_name == 'dica_carreira_dia':
        processor = DicaCarreiraDiaProcessor()
        result = processor.process_dica()
        print(f"Generated: {result.get('title', 'Unknown')}")
        if upload:
            if 'video_path' in result:
                upload_video({'video_path': result['video_path'], 'title': result['title'], 'description': result['description'], 'tags': result['tags']}, channel_name='dica_carreira_dia')
            if 'short_video_path' in result:
                upload_video({'video_path': result['short_video_path'], 'title': result['title'].replace(' | Dica de Carreira do Dia', ' | Shorts'), 'description': result['description'], 'tags': result['tags']}, channel_name='dica_carreira_dia')
    else:
        print(f"Unknown channel: {channel_name}")
        print(f"Available channels: {', '.join(CHANNELS)}")


def upload_video(result: dict, channel_name: str = None):
    """Upload video to YouTube.
    
    Args:
        result: Dictionary with video information
        channel_name: Channel identifier (e.g., 'explicado_shorts')
    """
    try:
        import yaml
        
        # Load channel config
        config_path = PROJECT_ROOT / 'config' / 'youtube_channels.yaml'
        category_id = "22"  # default
        credentials_path = None
        if config_path.exists() and channel_name:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                channel_config = config.get('channels', {}).get(channel_name, {})
                category_id = channel_config.get('category_id', category_id)
                credentials_path = channel_config.get('credentials_path')
                # Palavras-chave na descrição para SEO/descoberta
                keywords = channel_config.get('description_keywords', '')
                if keywords and result.get('description'):
                    result['description'] = result['description'].rstrip() + f"\n\nPalavras-chave: {keywords}"
                # Merge default tags
                default_tags = channel_config.get('default_tags', [])
                if result.get('tags'):
                    result['tags'] = list(set(result['tags'] + default_tags))
                else:
                    result['tags'] = default_tags
        
        # Use channel-specific credentials if configured (para uploads em canais separados)
        creds_file = PROJECT_ROOT / "config" / "client_secrets.json"
        creds_pickle = PROJECT_ROOT / "config" / f"credentials_{channel_name}.pickle" if channel_name else PROJECT_ROOT / "config" / "credentials.pickle"
        if credentials_path:
            candidate = PROJECT_ROOT / credentials_path
            if candidate.exists():
                creds_file = candidate
        # YouTubeUploader aceita str
        uploader = YouTubeUploader(
            client_secrets_file=str(creds_file),
            credentials_file=str(creds_pickle)
        )
        upload_result = uploader.upload_video(
            video_path=result['video_path'],
            title=result['title'],
            description=result['description'],
            tags=result['tags'],
            category_id=category_id,
            privacy_status='public',
            check_duplicate=True,
            channel_name=channel_name
        )
        
        if upload_result:
            if 'video_id' in upload_result:
                print(f"✅ Uploaded para {channel_name or 'canal padrão'}: {result['title']}")
                print(f"   URL: {upload_result.get('url', 'N/A')}")
            else:
                print(f"⚠️  Video já existe: {result['title']}")
        else:
            print(f"⚠️  Video já existe no YouTube: {result['title']}")
    except Exception as e:
        print(f"❌ Error uploading video: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='YouTube Content Automation')
    parser.add_argument(
        '--channel',
        type=str,
        required=True,
        choices=CHANNELS,
        help='Channel to process'
    )
    parser.add_argument(
        '--upload',
        action='store_true',
        help='Upload videos to YouTube'
    )
    
    args = parser.parse_args()
    process_channel(args.channel, args.upload)


if __name__ == '__main__':
    main()
