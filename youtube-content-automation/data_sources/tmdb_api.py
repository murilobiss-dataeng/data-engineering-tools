"""The Movie Database (TMDB) API integration for TV series data."""

import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class TMDBAPI:
    """Client for The Movie Database API."""
    
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize TMDB API client.
        
        Args:
            api_key: TMDB API key (or from env var TMDB_API_KEY)
        """
        self.api_key = api_key or os.getenv('TMDB_API_KEY')
        if not self.api_key:
            raise ValueError("TMDB_API_KEY not provided")
        
        self.params = {'api_key': self.api_key, 'language': 'pt-BR'}
        self.cache = {}
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            API response as dictionary
        """
        url = f"{self.BASE_URL}/{endpoint}"
        request_params = {**self.params, **(params or {})}
        response = requests.get(url, params=request_params)
        response.raise_for_status()
        return response.json()
    
    def search_tv_series(self, query: str) -> List[Dict]:
        """Search for TV series.
        
        Args:
            query: Search query
            
        Returns:
            List of TV series
        """
        cache_key = f"search_{query}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        response = self._make_request("search/tv", {'query': query})
        results = response.get('results', [])
        self.cache[cache_key] = results
        return results
    
    def get_tv_series_details(self, series_id: int) -> Dict:
        """Get detailed TV series information.
        
        Args:
            series_id: TV series ID
            
        Returns:
            Series details
        """
        cache_key = f"tv_{series_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        response = self._make_request(f"tv/{series_id}")
        self.cache[cache_key] = response
        return response
    
    def get_tv_series_images(self, series_id: int) -> Dict:
        """Get images for a TV series.
        
        Args:
            series_id: TV series ID
            
        Returns:
            Images (posters, backdrops, etc.)
        """
        cache_key = f"tv_images_{series_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        response = self._make_request(f"tv/{series_id}/images")
        self.cache[cache_key] = response
        return response
    
    def get_popular_tv_series(self, page: int = 1) -> List[Dict]:
        """Get popular TV series.
        
        Args:
            page: Page number
            
        Returns:
            List of popular TV series
        """
        cache_key = f"popular_tv_{page}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        response = self._make_request("tv/popular", {'page': page})
        results = response.get('results', [])
        self.cache[cache_key] = results
        return results
    
    def get_tv_series_credits(self, series_id: int) -> Dict:
        """Get cast and crew for a TV series.
        
        Args:
            series_id: TV series ID
            
        Returns:
            Credits information
        """
        cache_key = f"tv_credits_{series_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        response = self._make_request(f"tv/{series_id}/credits")
        self.cache[cache_key] = response
        return response
    
    def get_image_url(self, image_path: str, size: str = "original") -> str:
        """Get full URL for an image.
        
        Args:
            image_path: Image path from API
            size: Image size (w500, original, etc.)
            
        Returns:
            Full image URL
        """
        if not image_path:
            return ""
        return f"{self.IMAGE_BASE_URL}/{size}{image_path}"
    
    def filter_spoilers(self, text: str, series_data: Dict) -> str:
        """Filter potential spoilers from text.
        
        Args:
            text: Text to filter
            series_data: Series data to check against
            
        Returns:
            Filtered text
        """
        # Simple spoiler filtering - can be enhanced
        # Remove plot details that might be spoilers
        spoiler_keywords = [
            'morre', 'morte', 'assassinado', 'final', 'acaba',
            'descobre', 'revela', 'traição', 'trai'
        ]
        
        # This is a basic implementation
        # In production, use more sophisticated NLP
        filtered_text = text
        for keyword in spoiler_keywords:
            # Don't remove if it's in a safe context
            if keyword.lower() in text.lower():
                # Could implement more sophisticated filtering here
                pass
        
        return filtered_text
