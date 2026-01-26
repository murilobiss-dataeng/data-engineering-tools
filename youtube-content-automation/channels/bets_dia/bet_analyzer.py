"""Analyze betting opportunities and generate suggestions."""

from typing import Dict, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from data_sources.football_api import FootballAPI


class BetAnalyzer:
    """Analyze betting opportunities."""
    
    ADULT_WARNING = "⚠️ CONTEÚDO PARA MAIORES DE 18 ANOS ⚠️\n\n"
    ADULT_WARNING += "Este vídeo contém análises de apostas esportivas.\n"
    ADULT_WARNING += "Apostas envolvem risco de perda financeira.\n"
    ADULT_WARNING += "Jogue com responsabilidade.\n\n"
    
    def __init__(self, football_api: FootballAPI):
        """Initialize bet analyzer.
        
        Args:
            football_api: FootballAPI instance
        """
        self.football_api = football_api
    
    def analyze_match_for_betting(self, fixture_id: int) -> Dict:
        """Analyze a match for betting opportunities.
        
        Args:
            fixture_id: Fixture ID
            
        Returns:
            Betting analysis dictionary
        """
        match = self.football_api.get_match_details(fixture_id)
        statistics = self.football_api.get_match_statistics(fixture_id)
        standings = None
        
        if not match:
            return {}
        
        teams = match.get('teams', {})
        home_team = teams.get('home', {})
        away_team = teams.get('away', {})
        
        # Get team statistics
        home_team_id = home_team.get('id')
        away_team_id = away_team.get('id')
        
        # Analyze statistics
        home_stats = {}
        away_stats = {}
        if statistics:
            for stat in statistics.get('statistics', []):
                team_id = stat.get('team', {}).get('id')
                if team_id == home_team_id:
                    home_stats = stat
                elif team_id == away_team_id:
                    away_stats = stat
        
        # Calculate probabilities (simplified)
        home_win_prob = 0.4
        draw_prob = 0.3
        away_win_prob = 0.3
        
        # Analyze form (simplified - in production, use historical data)
        home_form = "Boa"
        away_form = "Regular"
        
        # Generate suggestions
        suggestions = []
        
        # Over 2.5 goals suggestion
        if self._calculate_over_under_probability(home_stats, away_stats) > 0.5:
            suggestions.append({
                'type': 'Over 2.5',
                'confidence': 'Média',
                'reason': 'Ambos os times têm histórico ofensivo'
            })
        
        # Both teams to score
        if self._calculate_btts_probability(home_stats, away_stats) > 0.5:
            suggestions.append({
                'type': 'Ambos marcam',
                'confidence': 'Média',
                'reason': 'Times com boa capacidade ofensiva'
            })
        
        return {
            'fixture_id': fixture_id,
            'home_team': home_team.get('name', ''),
            'away_team': away_team.get('name', ''),
            'home_win_prob': home_win_prob,
            'draw_prob': draw_prob,
            'away_win_prob': away_win_prob,
            'home_form': home_form,
            'away_form': away_form,
            'suggestions': suggestions,
            'statistics': {
                'home': home_stats,
                'away': away_stats
            }
        }
    
    def _calculate_over_under_probability(self, home_stats: Dict, away_stats: Dict) -> float:
        """Calculate probability of over 2.5 goals."""
        # Simplified calculation
        return 0.55
    
    def _calculate_btts_probability(self, home_stats: Dict, away_stats: Dict) -> float:
        """Calculate probability of both teams to score."""
        # Simplified calculation
        return 0.60
    
    def generate_bet_script(self, analysis: Dict, video_type: str = 'short') -> str:
        """Generate script for betting analysis video.
        
        Args:
            analysis: Betting analysis dictionary
            video_type: 'short' or 'long'
            
        Returns:
            Generated script
        """
        script = self.ADULT_WARNING
        
        home_team = analysis.get('home_team', '')
        away_team = analysis.get('away_team', '')
        
        script += f"Análise para o jogo: {home_team} vs {away_team}\n\n"
        
        if video_type == 'short':
            script += "Principais sugestões:\n\n"
            suggestions = analysis.get('suggestions', [])
            for i, suggestion in enumerate(suggestions[:2], 1):
                script += f"{i}. {suggestion['type']}\n"
                script += f"   Confiança: {suggestion['confidence']}\n\n"
            
            script += "⚠️ Lembre-se: apostas envolvem risco!\n"
            script += "Jogue com responsabilidade."
        else:
            script += "Análise completa:\n\n"
            
            script += f"Probabilidades:\n"
            script += f"- Vitória {home_team}: {analysis.get('home_win_prob', 0)*100:.0f}%\n"
            script += f"- Empate: {analysis.get('draw_prob', 0)*100:.0f}%\n"
            script += f"- Vitória {away_team}: {analysis.get('away_win_prob', 0)*100:.0f}%\n\n"
            
            script += "Sugestões de apostas:\n\n"
            suggestions = analysis.get('suggestions', [])
            for i, suggestion in enumerate(suggestions, 1):
                script += f"{i}. {suggestion['type']}\n"
                script += f"   Confiança: {suggestion['confidence']}\n"
                script += f"   Motivo: {suggestion['reason']}\n\n"
            
            script += "⚠️ AVISOS IMPORTANTES:\n"
            script += "- Apostas envolvem risco de perda financeira\n"
            script += "- Nunca aposte mais do que pode perder\n"
            script += "- Jogue com responsabilidade\n"
            script += "- Este conteúdo é apenas para fins informativos\n\n"
            script += "Não esqueça de se inscrever e deixar seu like!"
        
        return script
