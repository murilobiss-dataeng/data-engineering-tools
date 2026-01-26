"""Airflow DAG for Placar do Dia channel."""

import os
import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from channels.placar_dia.channel_processor import PlacarDiaProcessor
from core.youtube_uploader import YouTubeUploader


def process_placar_dia():
    """Process Placar do Dia content."""
    processor = PlacarDiaProcessor()
    results = processor.process_round()
    
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
                    privacy_status='public'
                )
                print(f"Uploaded: {result['title']}")
            except Exception as e:
                print(f"Error uploading {result['title']}: {e}")
        
        if 'short_video_path' in result:
            try:
                short_title = result['title'].replace(' - Resumo Completo', ' - Shorts')
                uploader.upload_video(
                    video_path=result['short_video_path'],
                    title=short_title,
                    description=result['description'],
                    tags=result['tags'],
                    privacy_status='public'
                )
                print(f"Uploaded short: {short_title}")
            except Exception as e:
                print(f"Error uploading short: {e}")


default_args = {
    'owner': 'youtube-automation',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'placar_dia_dag',
    default_args=default_args,
    description='Generate and upload Placar do Dia videos',
    schedule_interval='0 20 * * *',  # Daily at 8 PM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['youtube', 'placar_dia', 'football']
)

process_task = PythonOperator(
    task_id='process_placar_dia',
    python_callable=process_placar_dia,
    dag=dag
)
