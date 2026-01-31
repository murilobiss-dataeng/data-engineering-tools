# Exemplos de Uso

## Exemplo 1: Gerar vídeo do Placar do Dia

```python
from channels.placar_dia.channel_processor import PlacarDiaProcessor

processor = PlacarDiaProcessor()
results = processor.process_round()

for result in results:
    print(f"Vídeo gerado: {result['title']}")
    print(f"Caminho: {result.get('video_path', 'N/A')}")
```

## Exemplo 2: Gerar vídeo educacional

```python
from channels.explicado_shorts.channel_processor import ExplicadoShortsProcessor

processor = ExplicadoShortsProcessor()
result = processor.process_topic(topic="O que é Inteligência Artificial?")

print(f"Vídeo gerado: {result['title']}")
```

## Exemplo 4: Gerar vídeo de simulação financeira

```python
from channels.quanto_rende.channel_processor import QuantoRendeProcessor

processor = QuantoRendeProcessor()
result = processor.process_investment(
    investment={
        'type': 'CDB',
        'principal': 10000,
        'period_months': 12
    }
)

print(f"Vídeo gerado: {result['title']}")
```

## Exemplo 4: Gerar vídeo sobre série

```python
from channels.series_explicadas.channel_processor import SeriesExplicadasProcessor

processor = SeriesExplicadasProcessor()
result = processor.process_series(series_id=1396)  # Game of Thrones

print(f"Vídeo gerado: {result['title']}")
```

## Exemplo 5: Upload manual para YouTube

```python
from core.youtube_uploader import YouTubeUploader

uploader = YouTubeUploader()
result = uploader.upload_video(
    video_path="outputs/video.mp4",
    title="Meu Vídeo",
    description="Descrição do vídeo",
    tags=["tag1", "tag2"],
    privacy_status="private"  # ou "public" ou "unlisted"
)

print(f"Vídeo ID: {result['video_id']}")
print(f"URL: {result['url']}")
```

## Exemplo 6: Pipeline completo (gerar + upload)

```python
from channels.placar_dia.channel_processor import PlacarDiaProcessor
from core.youtube_uploader import YouTubeUploader

# Gerar vídeo
processor = PlacarDiaProcessor()
result = processor.process_match(fixture_id=12345)

# Upload
if 'video_path' in result:
    uploader = YouTubeUploader()
    upload_result = uploader.upload_video(
        video_path=result['video_path'],
        title=result['title'],
        description=result['description'],
        tags=result['tags'],
        privacy_status='private'
    )
    print(f"Upload concluído: {upload_result['url']}")
```
