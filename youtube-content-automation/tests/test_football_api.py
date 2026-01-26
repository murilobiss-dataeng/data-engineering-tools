"""Test script for Football API."""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# Load environment variables
load_dotenv(project_root / 'config' / 'api_keys.env')

from data_sources.football_api import FootballAPI


def test_api():
    """Test Football API connection."""
    try:
        print("Testing Football API connection...")
        api_key = os.getenv('API_FOOTBALL_KEY')
        print(f"API Key: {api_key[:10]}..." if api_key else "API Key not found")
        
        api = FootballAPI()
        
        # Test 1: Get leagues for Brazil
        print("\n1. Testing get_leagues('Brazil')...")
        leagues = api.get_leagues("Brazil")
        print(f"   Found {len(leagues)} leagues")
        if leagues:
            print(f"   First league: {leagues[0].get('league', {}).get('name', 'N/A')}")
        
        # Test 2: Get today's fixtures
        # Get league_id from config or use default
        league_id = int(os.getenv('FOOTBALL_LEAGUE_ID', '71'))
        print(f"\n2. Testing get_fixtures(league_id={league_id})...")
        fixtures = api.get_fixtures(league_id=league_id)
        print(f"   Found {len(fixtures)} fixtures for today")
        if fixtures:
            fixture = fixtures[0]
            teams = fixture.get('teams', {})
            home = teams.get('home', {}).get('name', 'N/A')
            away = teams.get('away', {}).get('name', 'N/A')
            print(f"   Example: {home} vs {away}")
        
        # Test 3: Get standings
        print(f"\n3. Testing get_standings(league_id={league_id})...")
        standings = api.get_standings(league_id=league_id)
        print(f"   Found {len(standings)} standings entries")
        
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
