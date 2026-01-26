"""Financial data APIs for investment calculations."""

import os
import requests
from typing import Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class FinancialAPI:
    """Client for financial data APIs."""
    
    def __init__(self):
        """Initialize Financial API client."""
        self.cache = {}
    
    def get_cdi_rate(self, date: Optional[str] = None) -> float:
        """Get CDI (Certificado de Depósito Interbancário) rate.
        
        Args:
            date: Date in YYYY-MM-DD format (default: today)
            
        Returns:
            CDI rate as percentage
        """
        # Using BCB (Banco Central do Brasil) API
        # This is a simplified version - in production, use official API
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cache_key = f"cdi_{date}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Placeholder - replace with actual API call
        # BCB API endpoint: https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados
        try:
            url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados/ultimos/1"
            response = requests.get(url, params={'formato': 'json'})
            if response.status_code == 200:
                data = response.json()
                if data:
                    rate = float(data[0]['valor'])
                    self.cache[cache_key] = rate
                    return rate
        except Exception as e:
            print(f"Error fetching CDI rate: {e}")
        
        # Default fallback rate
        default_rate = 13.65  # Approximate CDI rate
        self.cache[cache_key] = default_rate
        return default_rate
    
    def get_selic_rate(self, date: Optional[str] = None) -> float:
        """Get SELIC rate.
        
        Args:
            date: Date in YYYY-MM-DD format (default: today)
            
        Returns:
            SELIC rate as percentage
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cache_key = f"selic_{date}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # BCB API for SELIC
        try:
            url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1"
            response = requests.get(url, params={'formato': 'json'})
            if response.status_code == 200:
                data = response.json()
                if data:
                    rate = float(data[0]['valor'])
                    self.cache[cache_key] = rate
                    return rate
        except Exception as e:
            print(f"Error fetching SELIC rate: {e}")
        
        # Default fallback rate
        default_rate = 10.50  # Approximate SELIC rate
        self.cache[cache_key] = default_rate
        return default_rate
    
    def calculate_investment_return(
        self,
        principal: float,
        rate: float,
        period_months: int,
        tax_rate: float = 0.15
    ) -> Dict:
        """Calculate investment return with taxes.
        
        Args:
            principal: Initial investment amount
            rate: Annual interest rate (as percentage)
            period_months: Investment period in months
            tax_rate: Tax rate (default 15% for long-term investments)
            
        Returns:
            Dictionary with calculation results
        """
        # Convert annual rate to monthly
        monthly_rate = (1 + rate / 100) ** (1 / 12) - 1
        
        # Calculate compound interest
        final_amount = principal * ((1 + monthly_rate) ** period_months)
        
        # Calculate profit
        profit = final_amount - principal
        
        # Calculate taxes (only on profit)
        tax_amount = profit * tax_rate
        
        # Net amount after taxes
        net_amount = final_amount - tax_amount
        
        # Net profit
        net_profit = net_amount - principal
        
        return {
            'principal': principal,
            'final_amount': final_amount,
            'profit': profit,
            'tax_amount': tax_amount,
            'net_amount': net_amount,
            'net_profit': net_profit,
            'monthly_rate': monthly_rate * 100,
            'period_months': period_months,
            'rate': rate
        }
    
    def calculate_cdb_return(
        self,
        principal: float,
        cdi_percentage: float,
        period_months: int
    ) -> Dict:
        """Calculate CDB investment return.
        
        Args:
            principal: Initial investment amount
            cdi_percentage: CDI percentage (e.g., 100 for 100% of CDI)
            period_months: Investment period in months
            
        Returns:
            Dictionary with calculation results
        """
        cdi_rate = self.get_cdi_rate()
        effective_rate = cdi_rate * (cdi_percentage / 100)
        
        # CDB tax rates: 22.5% (up to 180 days), 20% (181-360), 
        # 17.5% (361-720), 15% (over 720 days)
        if period_months <= 6:
            tax_rate = 0.225
        elif period_months <= 12:
            tax_rate = 0.20
        elif period_months <= 24:
            tax_rate = 0.175
        else:
            tax_rate = 0.15
        
        return self.calculate_investment_return(
            principal, effective_rate, period_months, tax_rate
        )
