"""Calculate betting risks and probabilities."""

from typing import Dict, List
import statistics


class RiskCalculator:
    """Calculate betting risks and probabilities."""
    
    def calculate_kelly_criterion(
        self,
        probability: float,
        odds: float,
        bankroll: float = 1000.0
    ) -> Dict:
        """Calculate Kelly Criterion for bet sizing.
        
        Args:
            probability: Probability of winning (0-1)
            odds: Decimal odds
            bankroll: Current bankroll
            
        Returns:
            Dictionary with Kelly calculation results
        """
        # Kelly formula: f = (bp - q) / b
        # where f = fraction of bankroll, b = odds - 1, p = probability, q = 1 - p
        b = odds - 1
        p = probability
        q = 1 - p
        
        if b <= 0 or p <= 0:
            return {
                'kelly_fraction': 0,
                'recommended_bet': 0,
                'expected_value': 0,
                'risk_level': 'High'
            }
        
        kelly_fraction = (b * p - q) / b
        
        # Limit to 25% of bankroll (conservative approach)
        kelly_fraction = min(kelly_fraction, 0.25)
        kelly_fraction = max(kelly_fraction, 0)  # No negative bets
        
        recommended_bet = bankroll * kelly_fraction
        
        # Calculate expected value
        expected_value = (probability * odds - 1) * recommended_bet
        
        # Determine risk level
        if kelly_fraction > 0.15:
            risk_level = 'High'
        elif kelly_fraction > 0.05:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        return {
            'kelly_fraction': kelly_fraction,
            'recommended_bet': recommended_bet,
            'expected_value': expected_value,
            'risk_level': risk_level,
            'probability': probability,
            'odds': odds
        }
    
    def calculate_expected_value(
        self,
        probability: float,
        odds: float,
        stake: float
    ) -> Dict:
        """Calculate expected value of a bet.
        
        Args:
            probability: Probability of winning
            odds: Decimal odds
            stake: Bet stake
            
        Returns:
            Dictionary with EV calculation
        """
        win_amount = stake * (odds - 1)
        loss_amount = stake
        
        expected_value = (probability * win_amount) - ((1 - probability) * loss_amount)
        roi = (expected_value / stake) * 100 if stake > 0 else 0
        
        return {
            'expected_value': expected_value,
            'roi': roi,
            'win_amount': win_amount,
            'loss_amount': loss_amount,
            'probability': probability,
            'odds': odds
        }
    
    def calculate_parlay_risk(
        self,
        bets: List[Dict]
    ) -> Dict:
        """Calculate risk for a parlay bet.
        
        Args:
            bets: List of bet dictionaries with 'probability' and 'odds'
            
        Returns:
            Dictionary with parlay risk analysis
        """
        if not bets:
            return {}
        
        # Calculate combined probability
        combined_prob = 1.0
        combined_odds = 1.0
        
        for bet in bets:
            combined_prob *= bet.get('probability', 0)
            combined_odds *= bet.get('odds', 1)
        
        # Calculate expected value for $100 stake
        stake = 100
        win_amount = stake * (combined_odds - 1)
        loss_amount = stake
        
        expected_value = (combined_prob * win_amount) - ((1 - combined_prob) * loss_amount)
        
        return {
            'combined_probability': combined_prob,
            'combined_odds': combined_odds,
            'expected_value': expected_value,
            'risk_level': 'Very High' if combined_prob < 0.3 else 'High',
            'number_of_bets': len(bets)
        }
