"""Analyze TV series and generate spoiler-free explanations."""

from typing import Dict, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from data_sources.tmdb_api import TMDBAPI


class SeriesAnalyzer:
    """Analyze TV series and generate content."""
    
    def __init__(self):
        """Initialize series analyzer."""
        self.tmdb_api = TMDBAPI()
    
    def get_popular_series(self, limit: int = 10) -> List[Dict]:
        """Get popular TV series.
        
        Args:
            limit: Number of series to return
            
        Returns:
            List of popular series
        """
        series_list = []
        page = 1
        
        while len(series_list) < limit:
            results = self.tmdb_api.get_popular_tv_series(page)
            if not results:
                break
            
            series_list.extend(results[:limit - len(series_list)])
            page += 1
        
        return series_list[:limit]
    
    def get_random_series(self) -> Dict:
        """Get a random popular series.
        
        Returns:
            Series dictionary
        """
        series_list = self.get_popular_series(1)
        return series_list[0] if series_list else {}
    
    def analyze_series(self, series_id: int) -> Dict:
        """Analyze a TV series.
        
        Args:
            series_id: TMDB series ID
            
        Returns:
            Series analysis dictionary
        """
        series_data = self.tmdb_api.get_tv_series_details(series_id)
        images = self.tmdb_api.get_tv_series_images(series_id)
        credits = self.tmdb_api.get_tv_series_credits(series_id)
        
        if not series_data:
            return {}
        
        # Filter spoilers from overview
        overview = series_data.get('overview', '')
        filtered_overview = self.tmdb_api.filter_spoilers(overview, series_data)
        
        # Get poster image
        poster_path = series_data.get('poster_path', '')
        poster_url = self.tmdb_api.get_image_url(poster_path, 'w500') if poster_path else ''
        
        # Get main cast
        cast = credits.get('cast', [])[:5] if credits else []
        
        return {
            'series_id': series_id,
            'name': series_data.get('name', ''),
            'original_name': series_data.get('original_name', ''),
            'overview': filtered_overview,
            'first_air_date': series_data.get('first_air_date', ''),
            'genres': [g.get('name', '') for g in series_data.get('genres', [])],
            'vote_average': series_data.get('vote_average', 0),
            'number_of_seasons': series_data.get('number_of_seasons', 0),
            'number_of_episodes': series_data.get('number_of_episodes', 0),
            'poster_url': poster_url,
            'cast': [{'name': c.get('name', ''), 'character': c.get('character', '')} for c in cast],
            'production_companies': [c.get('name', '') for c in series_data.get('production_companies', [])]
        }
    
    def generate_series_script(self, analysis: Dict, video_type: str = 'short') -> str:
        """Generate script for series explanation video.
        
        Args:
            analysis: Series analysis dictionary
            video_type: 'short' or 'long'
            
        Returns:
            Generated script
        """
        name = analysis.get('name', '')
        overview = analysis.get('overview', '')
        genres = analysis.get('genres', [])
        first_air_date = analysis.get('first_air_date', '')
        vote_average = analysis.get('vote_average', 0)
        
        if video_type == 'short':
            script = f"Series Explicadas: {name}\n\n"
            script += f"{overview[:200]}...\n\n" if len(overview) > 200 else f"{overview}\n\n"
            script += f"Gênero: {', '.join(genres[:2])}\n"
            script += f"Avaliação: {vote_average:.1f}/10\n\n"
            script += "Confira o vídeo completo para mais detalhes!"
        else:
            script = f"Olá! Bem-vindo ao Series Explicadas!\n\n"
            script += f"Hoje vamos falar sobre: {name}\n\n"
            
            if overview:
                script += f"Sinopse:\n{overview}\n\n"
            
            if genres:
                script += f"Gêneros: {', '.join(genres)}\n\n"
            
            if first_air_date:
                script += f"Estreia: {first_air_date}\n\n"
            
            script += f"Avaliação: {vote_average:.1f}/10\n\n"
            
            script += "⚠️ Este vídeo não contém spoilers!\n"
            script += "Apenas informações gerais sobre a série.\n\n"
            script += "Não esqueça de se inscrever e deixar seu like!"
        
        return script
