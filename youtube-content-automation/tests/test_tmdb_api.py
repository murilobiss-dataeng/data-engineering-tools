"""Test script for TMDB API."""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# Load environment variables
load_dotenv(project_root / 'config' / 'api_keys.env')

from data_sources.tmdb_api import TMDBAPI


def test_api():
    """Test TMDB API connection."""
    try:
        print("Testing TMDB API connection...")
        api_key = os.getenv('TMDB_API_KEY')
        print(f"API Key: {api_key[:10]}..." if api_key else "API Key not found")
        
        api = TMDBAPI()
        
        # Test 1: Search for a popular TV series
        print("\n1. Testing search_tv_series('Game of Thrones')...")
        results = api.search_tv_series("Game of Thrones")
        print(f"   Found {len(results)} results")
        if results:
            series = results[0]
            print(f"   First result: {series.get('name', 'N/A')} (ID: {series.get('id', 'N/A')})")
            series_id = series.get('id')
        
        # Test 2: Get series details
        if results:
            print(f"\n2. Testing get_tv_series_details(series_id={series_id})...")
            details = api.get_tv_series_details(series_id)
            print(f"   Series: {details.get('name', 'N/A')}")
            print(f"   Overview: {details.get('overview', 'N/A')[:100]}...")
            print(f"   First air date: {details.get('first_air_date', 'N/A')}")
            print(f"   Number of seasons: {details.get('number_of_seasons', 'N/A')}")
        
        # Test 3: Get popular TV series
        print("\n3. Testing get_popular_tv_series()...")
        popular = api.get_popular_tv_series(page=1)
        print(f"   Found {len(popular)} popular series")
        if popular:
            print(f"   Top series: {popular[0].get('name', 'N/A')}")
        
        # Test 4: Get series images
        if results:
            print(f"\n4. Testing get_tv_series_images(series_id={series_id})...")
            images = api.get_tv_series_images(series_id)
            posters = images.get('posters', [])
            print(f"   Found {len(posters)} poster images")
            if posters:
                poster_url = api.get_image_url(posters[0].get('file_path', ''), 'w500')
                print(f"   Poster URL: {poster_url[:80]}...")
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_api()
    sys.exit(0 if success else 1)
