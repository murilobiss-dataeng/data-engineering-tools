"""Main entry point for YouTube content automation."""

import argparse
import sys
import os
from dotenv import load_dotenv

load_dotenv('config/api_keys.env')

# Import channel processors
from channels.placar_dia.channel_processor import PlacarDiaProcessor
from channels.bets_dia.channel_processor import BetsDiaProcessor
from channels.explicado_shorts.channel_processor import ExplicadoShortsProcessor
from channels.quanto_rende.channel_processor import QuantoRendeProcessor
from channels.series_explicadas.channel_processor import SeriesExplicadasProcessor
from core.youtube_uploader import YouTubeUploader


def process_channel(channel_name: str, upload: bool = False):
    """Process a specific channel.
    
    Args:
        channel_name: Name of the channel to process
        upload: Whether to upload to YouTube
    """
    print(f"Processing channel: {channel_name}")
    
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
    
    elif channel_name == 'bets_dia':
        processor = BetsDiaProcessor()
        # Get a fixture ID (in production, get from API)
        # For demo, using a placeholder
        result = processor.process_match_bet(fixture_id=12345)  # Replace with actual ID
        print(f"Generated: {result.get('title', 'Unknown')}")
        if upload:
            if 'video_path' in result:
                upload_video(result, channel_name='bets_dia')
            if 'short_video_path' in result:
                upload_video({
                    'video_path': result['short_video_path'],
                    'title': result['title'].replace(' | Bets do Dia', ' | Shorts'),
                    'description': result['description'],
                    'tags': result['tags']
                }, channel_name='bets_dia')
    
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
            # Upload long-form video
            if 'video_path' in result:
                upload_video({
                    'video_path': result['video_path'],
                    'title': result['title'],
                    'description': result['description'],
                    'tags': result['tags']
                }, channel_name='series_explicadas')
            # Upload shorts video
            if 'short_video_path' in result:
                short_title = result['title'].replace(' | Series Explicadas', ' | Shorts')
                upload_video({
                    'video_path': result['short_video_path'],
                    'title': short_title,
                    'description': result['description'],
                    'tags': result['tags']
                }, channel_name='series_explicadas')
    
    else:
        print(f"Unknown channel: {channel_name}")
        print("Available channels: placar_dia, bets_dia, explicado_shorts, quanto_rende, series_explicadas")


def upload_video(result: dict, channel_name: str = None):
    """Upload video to YouTube.
    
    Args:
        result: Dictionary with video information
        channel_name: Channel identifier (e.g., 'explicado_shorts')
    """
    try:
        import yaml
        
        # Load channel config
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'youtube_channels.yaml')
        category_id = "22"  # default
        if os.path.exists(config_path) and channel_name:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                channel_config = config.get('channels', {}).get(channel_name, {})
                category_id = channel_config.get('category_id', category_id)
                # Merge default tags
                default_tags = channel_config.get('default_tags', [])
                if result.get('tags'):
                    result['tags'] = list(set(result['tags'] + default_tags))
                else:
                    result['tags'] = default_tags
        
        uploader = YouTubeUploader()
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
        choices=['placar_dia', 'bets_dia', 'explicado_shorts', 'quanto_rende', 'series_explicadas'],
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
