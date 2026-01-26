"""Analyze football matches and generate summaries."""

from typing import Dict, List
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from data_sources.football_api import FootballAPI


class MatchAnalyzer:
    """Analyze football matches and generate content."""
    
    def __init__(self, football_api: FootballAPI):
        """Initialize match analyzer.
        
        Args:
            football_api: FootballAPI instance
        """
        self.football_api = football_api
    
    def get_round_matches(self, league_id: int, round: str = None) -> List[Dict]:
        """Get matches from a round.
        
        Args:
            league_id: League ID
            round: Round name (optional)
            
        Returns:
            List of matches
        """
        if round:
            return self.football_api.get_fixtures_by_round(league_id, round)
        else:
            # Get today's matches
            today = datetime.now().strftime('%Y-%m-%d')
            return self.football_api.get_fixtures(league_id, date=today)
    
    def analyze_match(self, fixture_id: int) -> Dict:
        """Analyze a single match.
        
        Args:
            fixture_id: Fixture ID
            
        Returns:
            Match analysis dictionary
        """
        match = self.football_api.get_match_details(fixture_id)
        events = self.football_api.get_match_events(fixture_id)
        statistics = self.football_api.get_match_statistics(fixture_id)
        
        if not match:
            return {}
        
        fixture = match.get('fixture', {})
        teams = match.get('teams', {})
        score = match.get('score', {})
        goals = match.get('goals', {})
        
        home_team = teams.get('home', {}).get('name', 'Time Casa')
        away_team = teams.get('away', {}).get('name', 'Time Visitante')
        home_score = goals.get('home')
        away_score = goals.get('away')
        
        # Analyze events
        goals_events = [e for e in events if e.get('type') == 'Goal']
        cards_events = [e for e in events if e.get('type') in ['Card', 'card']]
        
        # Get statistics
        home_stats = {}
        away_stats = {}
        if statistics:
            for stat in statistics.get('statistics', []):
                if stat.get('team', {}).get('id') == teams.get('home', {}).get('id'):
                    home_stats = stat
                elif stat.get('team', {}).get('id') == teams.get('away', {}).get('id'):
                    away_stats = stat
        
        return {
            'fixture_id': fixture_id,
            'home_team': home_team,
            'away_team': away_team,
            'home_score': home_score,
            'away_score': away_score,
            'status': fixture.get('status', {}).get('long', 'Não iniciado'),
            'date': fixture.get('date'),
            'venue': fixture.get('venue', {}).get('name', ''),
            'goals': len(goals_events),
            'cards': len(cards_events),
            'events': events,
            'statistics': {
                'home': home_stats,
                'away': away_stats
            }
        }
    
    def generate_match_summary(self, match_analysis: Dict) -> str:
        """Generate a text summary of the match.
        
        Args:
            match_analysis: Match analysis dictionary
            
        Returns:
            Text summary
        """
        home_team = match_analysis.get('home_team', 'Time Casa')
        away_team = match_analysis.get('away_team', 'Time Visitante')
        home_score = match_analysis.get('home_score')
        away_score = match_analysis.get('away_score')
        status = match_analysis.get('status', '')
        
        summary = f"Resumo do jogo: {home_team} vs {away_team}\n\n"
        
        if status == 'Match Finished':
            summary += f"Placar final: {home_team} {home_score} x {away_score} {away_team}\n\n"
            
            if home_score > away_score:
                summary += f"{home_team} venceu o jogo em casa!\n\n"
            elif away_score > home_score:
                summary += f"{away_team} venceu jogando fora de casa!\n\n"
            else:
                summary += "O jogo terminou empatado!\n\n"
            
            # Add goal details
            events = match_analysis.get('events', [])
            goals = [e for e in events if e.get('type') == 'Goal']
            
            if goals:
                summary += "Gols marcados:\n"
                for goal in goals[:5]:  # Limit to 5 goals
                    team = goal.get('team', {}).get('name', '')
                    player = goal.get('player', {}).get('name', '')
                    minute = goal.get('time', {}).get('elapsed', '')
                    summary += f"- {minute}': {player} ({team})\n"
                summary += "\n"
        else:
            summary += f"Status: {status}\n\n"
            if home_score is not None and away_score is not None:
                summary += f"Placar atual: {home_team} {home_score} x {away_score} {away_team}\n\n"
        
        summary += "Não esqueça de se inscrever e deixar seu like!"
        
        return summary
