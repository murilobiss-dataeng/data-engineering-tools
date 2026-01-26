"""Simulate investment returns and generate calculations."""

from typing import Dict, List
import random
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from data_sources.financial_api import FinancialAPI


class InvestmentSimulator:
    """Simulate investment returns."""
    
    INVESTMENT_TYPES = [
        'CDB',
        'LCI',
        'LCA',
        'Tesouro Direto',
        'Poupança',
        'Fundos de Investimento'
    ]
    
    def __init__(self):
        """Initialize investment simulator."""
        self.financial_api = FinancialAPI()
    
    def get_random_investment(self) -> Dict:
        """Get a random investment scenario.
        
        Returns:
            Investment scenario dictionary
        """
        investment_type = random.choice(self.INVESTMENT_TYPES)
        
        # Random principal amount
        principal = random.choice([1000, 5000, 10000, 50000, 100000])
        
        # Random period
        period_months = random.choice([6, 12, 24, 36, 60])
        
        return {
            'type': investment_type,
            'principal': principal,
            'period_months': period_months
        }
    
    def simulate_investment(self, investment: Dict) -> Dict:
        """Simulate an investment.
        
        Args:
            investment: Investment dictionary with type, principal, period_months
            
        Returns:
            Simulation results
        """
        investment_type = investment.get('type', 'CDB')
        principal = investment.get('principal', 10000)
        period_months = investment.get('period_months', 12)
        
        if investment_type == 'CDB':
            # CDB at 100% of CDI
            cdi_percentage = 100
            result = self.financial_api.calculate_cdb_return(
                principal, cdi_percentage, period_months
            )
            result['investment_type'] = 'CDB'
            result['cdi_percentage'] = cdi_percentage
        
        elif investment_type == 'Poupança':
            # Poupança rate (simplified)
            poupanca_rate = 6.17  # Approximate annual rate
            result = self.financial_api.calculate_investment_return(
                principal, poupanca_rate, period_months, tax_rate=0.0
            )
            result['investment_type'] = 'Poupança'
        
        elif investment_type == 'Tesouro Direto':
            # Treasury bond (simplified)
            selic_rate = self.financial_api.get_selic_rate()
            result = self.financial_api.calculate_investment_return(
                principal, selic_rate, period_months, tax_rate=0.15
            )
            result['investment_type'] = 'Tesouro Direto'
        
        else:
            # Generic investment
            rate = 12.0  # Default rate
            result = self.financial_api.calculate_investment_return(
                principal, rate, period_months, tax_rate=0.15
            )
            result['investment_type'] = investment_type
        
        return result
    
    def generate_explanation(self, simulation: Dict) -> str:
        """Generate explanation text for simulation.
        
        Args:
            simulation: Simulation results dictionary
            
        Returns:
            Explanation text
        """
        investment_type = simulation.get('investment_type', 'Investimento')
        principal = simulation.get('principal', 0)
        period_months = simulation.get('period_months', 0)
        net_amount = simulation.get('net_amount', 0)
        net_profit = simulation.get('net_profit', 0)
        rate = simulation.get('rate', 0)
        
        explanation = f"Simulação: {investment_type}\n\n"
        explanation += f"Valor inicial: R$ {principal:,.2f}\n"
        explanation += f"Prazo: {period_months} meses\n"
        explanation += f"Taxa anual: {rate:.2f}%\n\n"
        
        explanation += "Resultados:\n"
        explanation += f"Valor bruto: R$ {simulation.get('final_amount', 0):,.2f}\n"
        explanation += f"Impostos: R$ {simulation.get('tax_amount', 0):,.2f}\n"
        explanation += f"Valor líquido: R$ {net_amount:,.2f}\n"
        explanation += f"Lucro líquido: R$ {net_profit:,.2f}\n\n"
        
        roi = (net_profit / principal) * 100 if principal > 0 else 0
        explanation += f"Retorno sobre investimento: {roi:.2f}%\n\n"
        
        explanation += "⚠️ Esta é uma simulação baseada em taxas atuais.\n"
        explanation += "Valores reais podem variar.\n"
        explanation += "Consulte um consultor financeiro antes de investir."
        
        return explanation
