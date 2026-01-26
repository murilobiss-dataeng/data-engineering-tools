"""Airflow DAG for Bets do Dia channel."""

import os
import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from channels.bets_dia.channel_processor import BetsDiaProcessor
from data_sources.football_api import FootballAPI
from core.youtube_uploader import YouTubeUploader


def process_bets_dia():
    """Process Bets do Dia content."""
    processor = BetsDiaProcessor()
    football_api = FootballAPI()
    
    # Get today's matches
    from datetime import datetime
    import yaml
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get league_id from config
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'channels.yaml')
    league_id = 71  # default
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            league_id = config.get('placar_dia', {}).get('league_id', 71)
    
    fixtures = football_api.get_fixtures(league_id=league_id, date=today)
    
    # Process first 3 matches
    results = []
    for match in fixtures[:3]:
        fixture_id = match.get('fixture', {}).get('id')
        if fixture_id:
            result = processor.process_match_bet(fixture_id)
            if result:
                results.append(result)
    
    # Upload videos to YouTube
    uploader = YouTubeUploader()
    
    for result in results:
        if 'video_path' in result:
            try:
                uploader.upload_video(
                    video_path=result['video_path'],
                    title=result['title'],
                    description=result['description'],
                    tags=result['tags'],
                    category_id='22',  # People & Blogs
                    privacy_status='public'
                )
                print(f"Uploaded: {result['title']}")
            except Exception as e:
                print(f"Error uploading {result['title']}: {e}")


default_args = {
    'owner': 'youtube-automation',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'bets_dia_dag',
    default_args=default_args,
    description='Generate and upload Bets do Dia videos',
    schedule_interval='0 19 * * *',  # Daily at 7 PM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['youtube', 'bets_dia', 'betting', '18+']
)

process_task = PythonOperator(
    task_id='process_bets_dia',
    python_callable=process_bets_dia,
    dag=dag
)
