"""Test script to verify all imports work correctly."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...\n")
    
    errors = []
    
    # Test core modules
    print("1. Testing core modules...")
    try:
        from core.video_generator import VideoGenerator
        from core.template_engine import TemplateEngine
        from core.text_to_speech import TextToSpeech
        from core.youtube_uploader import YouTubeUploader
        from core.image_processor import ImageProcessor
        print("   ✅ Core modules imported successfully")
    except Exception as e:
        print(f"   ❌ Error importing core modules: {e}")
        errors.append(f"Core modules: {e}")
    
    # Test data sources
    print("\n2. Testing data sources...")
    try:
        from data_sources.football_api import FootballAPI
        from data_sources.tmdb_api import TMDBAPI
        from data_sources.financial_api import FinancialAPI
        from data_sources.content_generator import ContentGenerator
        print("   ✅ Data sources imported successfully")
    except Exception as e:
        print(f"   ❌ Error importing data sources: {e}")
        errors.append(f"Data sources: {e}")
    
    # Test channel processors
    print("\n3. Testing channel processors...")
    try:
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
        print("   ✅ Channel processors imported successfully")
    except Exception as e:
        print(f"   ❌ Error importing channel processors: {e}")
        errors.append(f"Channel processors: {e}")
    
    # Test configuration files
    print("\n4. Testing configuration files...")
    config_files = {
        'api_keys.env': project_root / 'config' / 'api_keys.env',
        'client_secrets.json': project_root / 'config' / 'client_secrets.json',
        'youtube_channels.yaml': project_root / 'config' / 'youtube_channels.yaml',
        'templates.yaml': project_root / 'config' / 'templates.yaml'
    }
    
    for name, path in config_files.items():
        if path.exists():
            print(f"   ✅ {name} exists")
        else:
            print(f"   ⚠️  {name} not found (may be optional)")
    
    # Summary
    print("\n" + "="*50)
    if errors:
        print("❌ Some imports failed:")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print("✅ All imports successful!")
        print("\n✅ System is ready to use!")
        return True


if __name__ == '__main__':
    success = test_imports()
    sys.exit(0 if success else 1)
