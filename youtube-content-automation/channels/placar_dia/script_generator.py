"""Generate scripts for match summary videos."""

from typing import Dict, List
from .match_analyzer import MatchAnalyzer


class ScriptGenerator:
    """Generate video scripts for match summaries."""
    
    def __init__(self, match_analyzer: MatchAnalyzer):
        """Initialize script generator.
        
        Args:
            match_analyzer: MatchAnalyzer instance
        """
        self.match_analyzer = match_analyzer
    
    def generate_match_script(self, fixture_id: int, video_type: str = 'short') -> Dict:
        """Generate script for a match video.
        
        Args:
            fixture_id: Fixture ID
            video_type: 'short' or 'long'
            
        Returns:
            Dictionary with script and metadata
        """
        match_analysis = self.match_analyzer.analyze_match(fixture_id)
        
        if not match_analysis:
            return {}
        
        home_team = match_analysis.get('home_team', 'Time Casa')
        away_team = match_analysis.get('away_team', 'Time Visitante')
        home_score = match_analysis.get('home_score')
        away_score = match_analysis.get('away_score')
        
        if video_type == 'short':
            script = self._generate_short_script(match_analysis)
        else:
            script = self._generate_long_script(match_analysis)
        
        title = f"{home_team} {home_score} x {away_score} {away_team} - Resumo Completo"
        
        description = f"Resumo completo do jogo entre {home_team} e {away_team}.\n\n"
        description += f"Placar: {home_team} {home_score} x {away_score} {away_team}\n\n"
        description += "Não esqueça de se inscrever e deixar seu like!"
        
        tags = [
            'futebol', 'placar', 'resumo', home_team, away_team,
            'brasileirão', 'campeonato', 'futebol brasileiro'
        ]
        
        return {
            'script': script,
            'title': title,
            'description': description,
            'tags': tags,
            'match_analysis': match_analysis
        }
    
    def _generate_short_script(self, match_analysis: Dict) -> str:
        """Generate short script (for shorts)."""
        home_team = match_analysis.get('home_team', 'Time Casa')
        away_team = match_analysis.get('away_team', 'Time Visitante')
        home_score = match_analysis.get('home_score')
        away_score = match_analysis.get('away_score')
        status = match_analysis.get('status', '')
        
        script = f"Placar do Dia: {home_team} vs {away_team}\n\n"
        
        if status == 'Match Finished':
            script += f"Resultado: {home_team} {home_score} x {away_score} {away_team}\n\n"
            
            if home_score > away_score:
                script += f"{home_team} venceu!\n\n"
            elif away_score > home_score:
                script += f"{away_team} venceu!\n\n"
            else:
                script += "Empate!\n\n"
        else:
            script += f"Status: {status}\n\n"
        
        script += "Confira o resumo completo no canal!"
        
        return script
    
    def _generate_long_script(self, match_analysis: Dict) -> str:
        """Generate long script (for long-form videos)."""
        summary = self.match_analyzer.generate_match_summary(match_analysis)
        
        script = "Olá! Bem-vindo ao Placar do Dia!\n\n"
        script += summary
        
        return script
