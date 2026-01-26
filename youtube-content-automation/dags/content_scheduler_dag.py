"""Airflow DAG for content scheduling (Explicado, Quanto Rende, Series)."""

import os
import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from channels.explicado_shorts.channel_processor import ExplicadoShortsProcessor
from channels.quanto_rende.channel_processor import QuantoRendeProcessor
from channels.series_explicadas.channel_processor import SeriesExplicadasProcessor
from core.youtube_uploader import YouTubeUploader


def process_explicado_shorts():
    """Process Explicado em Shorts content."""
    processor = ExplicadoShortsProcessor()
    result = processor.process_topic()
    
    if result and 'video_path' in result:
        uploader = YouTubeUploader()
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


def process_quanto_rende():
    """Process Quanto rende? content."""
    processor = QuantoRendeProcessor()
    result = processor.process_investment()
    
    if result and 'video_path' in result:
        uploader = YouTubeUploader()
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


def process_series_explicadas():
    """Process Series Explicadas content."""
    processor = SeriesExplicadasProcessor()
    result = processor.process_series()
    
    if result and 'video_path' in result:
        uploader = YouTubeUploader()
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


default_args = {
    'owner': 'youtube-automation',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# DAG for Explicado em Shorts (3x per week: Mon, Wed, Fri)
explicado_dag = DAG(
    'explicado_shorts_dag',
    default_args=default_args,
    description='Generate and upload Explicado em Shorts videos',
    schedule_interval='0 10 * * 1,3,5',  # Mon, Wed, Fri at 10 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['youtube', 'explicado_shorts', 'education']
)

explicado_task = PythonOperator(
    task_id='process_explicado_shorts',
    python_callable=process_explicado_shorts,
    dag=explicado_dag
)

# DAG for Quanto rende? (2x per week: Tue, Thu)
quanto_rende_dag = DAG(
    'quanto_rende_dag',
    default_args=default_args,
    description='Generate and upload Quanto rende? videos',
    schedule_interval='0 11 * * 2,4',  # Tue, Thu at 11 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['youtube', 'quanto_rende', 'finance']
)

quanto_rende_task = PythonOperator(
    task_id='process_quanto_rende',
    python_callable=process_quanto_rende,
    dag=quanto_rende_dag
)

# DAG for Series Explicadas (2x per week: Sat, Sun)
series_dag = DAG(
    'series_explicadas_dag',
    default_args=default_args,
    description='Generate and upload Series Explicadas videos',
    schedule_interval='0 14 * * 6,0',  # Sat, Sun at 2 PM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['youtube', 'series_explicadas', 'tv']
)

series_task = PythonOperator(
    task_id='process_series_explicadas',
    python_callable=process_series_explicadas,
    dag=series_dag
)
