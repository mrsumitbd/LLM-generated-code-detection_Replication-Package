import json
from anthropic import Anthropic

class MarketIntelligence:
    """Container for comprehensive market intelligence."""
    
    def __init__(self):
        """Initialize the MarketIntelligence with Anthropic client and conversation history."""
        self.client = Anthropic()
        self.conversation_history = []
        self.model = "claude-3-5-sonnet-20241022"
        self.market_data = {}
        
    def add_market_data(self, data_type: str, data: dict) -> None:
        """Add market data to the intelligence container."""
        self.market_data[data_type] = data
        
    def get_market_data(self, data_type: str) -> dict:
        """Retrieve market data by type."""
        return self.market_data.get(data_type, {})
    
    def analyze_market(self, query: str) -> str:
        """Analyze market conditions using multi-turn conversation with Claude."""
        self.conversation_history.append({
            "role": "user",
            "content": query
        })
        
        system_prompt = """You are an expert market analyst with deep knowledge of financial markets, 
        economic trends, and business intelligence. Provide comprehensive, data-driven analysis and insights.
        When analyzing markets, consider multiple factors including:
        - Market trends and patterns
        - Economic indicators
        - Competitive landscape
        - Risk factors
        - Opportunities and threats
        - Historical context and future projections
        
        Provide clear, actionable insights with specific recommendations when appropriate."""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system_prompt,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def get_sector_analysis(self, sector: str) -> str:
        """Get detailed analysis for a specific market sector."""
        query = f"""Provide a comprehensive analysis of the {sector} sector including:
        1. Current market size and growth trends
        2. Key players and competitive dynamics
        3. Recent developments and disruptions
        4. Regulatory environment
        5. Investment opportunities and risks
        6. Future outlook and predictions"""
        
        return self.analyze_market(query)
    
    def compare_markets(self, market1: str, market2: str) -> str:
        """Compare two different markets or sectors."""
        query = f"""Compare and contrast {market1} and {market2} markets:
        1. Market size and growth rates
        2. Key differences in dynamics
        3. Competitive advantages of each
        4. Risk profiles
        5. Investment potential
        6. Which presents better opportunities and why"""
        
        return self.analyze_market(query)
    
    def get_trend_analysis(self, trend: str) -> str:
        """Analyze a specific market trend."""
        query = f"""Analyze the following market trend: {trend}
        1. What is driving this trend?
        2. Which sectors/companies are most affected?
        3. What are the implications?
        4. How long is this trend likely to persist?
        5. What are the opportunities and risks?
        6. What should investors/businesses do?"""
        
        return self.analyze_market(query)
    
    def get_investment_recommendation(self, investment_type: str, criteria: str = "") -> str:
        """Get investment recommendations based on type and criteria."""
        query = f"""Provide investment recommendations for {investment_type}.
        Additional criteria: {criteria if criteria else 'General analysis'}
        
        Please include:
        1. Current market conditions for this investment type
        2. Top opportunities
        3. Risk assessment
        4. Recommended allocation strategy
        5. Timeline and expected returns
        6. Key factors to monitor"""
        
        return self.analyze_market(query)
    
    def get_risk_assessment(self, asset_or_sector: str) -> str:
        """Assess risks for a specific asset or sector."""
        query = f"""Conduct a comprehensive risk assessment for {asset_or_sector}:
        1. Identify major risk factors
        2. Assess probability and impact of each risk
        3. Systemic vs idiosyncratic risks
        4. Correlation with other assets
        5. Mitigation strategies
        6. Overall risk rating and recommendation"""
        
        return self.analyze_market(query)
    
    def get_economic_outlook(self, timeframe: str = "next 12 months") -> str:
        """Get economic outlook and macroeconomic analysis."""
        query = f"""Provide an economic outlook for the {timeframe}:
        1. Key macroeconomic indicators and forecasts
        2. Central bank policies and their impact
        3. Inflation and interest rate expectations
        4. Currency and commodity trends
        5. Geopolitical risks
        6. Sector-specific implications
        7. Investment strategy recommendations"""
        
        return self.analyze_market(query)
    
    def clear_conversation(self) -> None:
        """Clear the conversation history for a fresh analysis."""
        self.conversation_history = []
    
    def get_conversation_history(self) -> list:
        """Get the current conversation history."""
        return self.conversation_history
    
    def export_analysis(self, filename: str = "market_analysis.json") -> None:
        """Export the conversation history and market data to a JSON file."""
        export_data = {
            "market_data": self.market_data,
            "conversation_history": self.conversation_history
        }
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)


def main():
    """Main function to demonstrate MarketIntelligence usage."""
    intelligence = MarketIntelligence()
    
    print("Market Intelligence Analysis System")
    print("=" * 50)
    
    print("\n1. Sector Analysis - Technology Sector")
    print("-" * 50)
    tech_analysis = intelligence.get_sector_analysis("technology")
    print(tech_analysis[:500] + "..." if len(tech_analysis) > 500 else tech_analysis)
    
    print("\n2. Trend Analysis - AI and Machine Learning")
    print("-" * 50)
    ai_trend = intelligence.get_trend_analysis("artificial intelligence and machine learning in enterprise")
    print(ai_trend[:500] + "..." if len(ai_trend) > 500 else ai_trend)
    
    print("\n3. Economic Outlook")
    print("-" * 50)
    outlook = intelligence.get_economic_outlook("next 6 months")
    print(outlook[:500] + "..." if len(outlook) > 500 else outlook)
    
    print("\n4. Risk Assessment - Tech Stocks")
    print("-" * 50)
    risk = intelligence.get_risk_assessment("technology stocks")
    print(risk[:500] + "..." if len(risk) > 500 else risk)
    
    print("\n5. Investment Recommendation")
    print("-" * 50)
    recommendation = intelligence.get_investment_recommendation("growth stocks", "tech sector focus")
    print(recommendation[:500] + "..." if len(recommendation) > 500 else recommendation)
    
    print("\n" + "=" * 50)
    print("Analysis complete. Conversation history preserved for follow-up questions.")


if __name__ == "__main__":
    main()