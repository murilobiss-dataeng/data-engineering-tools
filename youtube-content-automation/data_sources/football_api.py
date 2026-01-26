"""API-Football integration for match data."""

import os
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv

load_dotenv()


class FootballAPI:
    """Client for API-Football (api-sports.io)."""
    
    BASE_URL = "https://v3.football.api-sports.io"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Football API client.
        
        Args:
            api_key: API-Football key (or from env var API_FOOTBALL_KEY)
        """
        self.api_key = api_key or os.getenv('API_FOOTBALL_KEY')
        if not self.api_key:
            raise ValueError("API_FOOTBALL_KEY not provided")
        
        self.headers = {
            'x-apisports-key': self.api_key
        }
        self.cache = {}
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request with rate limiting.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            API response as dictionary
        """
        # Rate limiting
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        self.last_request_time = time.time()
        return response.json()
    
    def get_leagues(self, country: str = "Brazil") -> List[Dict]:
        """Get leagues by country.
        
        Args:
            country: Country name
            
        Returns:
            List of leagues
        """
        cache_key = f"leagues_{country}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        response = self._make_request("leagues", {"country": country})
        leagues = response.get('response', [])
        self.cache[cache_key] = leagues
        return leagues
    
    def get_fixtures(
        self,
        league_id: int,
        season: int = None,
        date: str = None
    ) -> List[Dict]:
        """Get fixtures for a league.
        
        Args:
            league_id: League ID
            season: Season year (e.g., 2024)
            date: Date in YYYY-MM-DD format (default: today)
            
        Returns:
            List of fixtures
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        if season is None:
            season = datetime.now().year
        
        cache_key = f"fixtures_{league_id}_{date}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        params = {
            'league': league_id,
            'season': season,
            'date': date
        }
        
        response = self._make_request("fixtures", params)
        fixtures = response.get('response', [])
        self.cache[cache_key] = fixtures
        return fixtures
    
    def get_fixtures_by_round(
        self,
        league_id: int,
        round: str,
        season: int = None
    ) -> List[Dict]:
        """Get fixtures for a specific round.
        
        Args:
            league_id: League ID
            round: Round name (e.g., "Regular Season - 1")
            season: Season year
            
        Returns:
            List of fixtures
        """
        if season is None:
            season = datetime.now().year
        
        cache_key = f"fixtures_round_{league_id}_{round}_{season}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        params = {
            'league': league_id,
            'season': season,
            'round': round
        }
        
        response = self._make_request("fixtures", params)
        fixtures = response.get('response', [])
        self.cache[cache_key] = fixtures
        return fixtures
    
    def get_match_details(self, fixture_id: int) -> Dict:
        """Get detailed match information.
        
        Args:
            fixture_id: Fixture ID
            
        Returns:
            Match details
        """
        cache_key = f"fixture_{fixture_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        params = {'id': fixture_id}
        response = self._make_request("fixtures", params)
        fixtures = response.get('response', [])
        
        if fixtures:
            match = fixtures[0]
            self.cache[cache_key] = match
            return match
        
        return {}
    
    def get_match_events(self, fixture_id: int) -> List[Dict]:
        """Get match events (goals, cards, etc.).
        
        Args:
            fixture_id: Fixture ID
            
        Returns:
            List of match events
        """
        cache_key = f"events_{fixture_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        params = {'fixture': fixture_id}
        response = self._make_request("fixtures/events", params)
        events = response.get('response', [])
        self.cache[cache_key] = events
        return events
    
    def get_match_statistics(self, fixture_id: int) -> Dict:
        """Get match statistics.
        
        Args:
            fixture_id: Fixture ID
            
        Returns:
            Match statistics
        """
        cache_key = f"stats_{fixture_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        params = {'fixture': fixture_id}
        response = self._make_request("fixtures/statistics", params)
        stats = response.get('response', [])
        
        if stats:
            statistics = stats[0]
            self.cache[cache_key] = statistics
            return statistics
        
        return {}
    
    def get_team_info(self, team_id: int) -> Dict:
        """Get team information.
        
        Args:
            team_id: Team ID
            
        Returns:
            Team information
        """
        cache_key = f"team_{team_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        params = {'id': team_id}
        response = self._make_request("teams", params)
        teams = response.get('response', [])
        
        if teams:
            team = teams[0]
            self.cache[cache_key] = team
            return team
        
        return {}
    
    def get_standings(self, league_id: int, season: int = None) -> List[Dict]:
        """Get league standings.
        
        Args:
            league_id: League ID
            season: Season year
            
        Returns:
            League standings
        """
        if season is None:
            season = datetime.now().year
        
        cache_key = f"standings_{league_id}_{season}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        params = {
            'league': league_id,
            'season': season
        }
        
        response = self._make_request("standings", params)
        standings = response.get('response', [])
        self.cache[cache_key] = standings
        return standings
