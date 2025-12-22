import anthropic
import json
from typing import Optional


class MarketData:
    """Container for market data and analysis."""

    def __init__(self, symbol: str, price: float, volume: int, market_cap: float):
        """Initialize MarketData with stock information.
        
        Args:
            symbol: Stock ticker symbol
            price: Current stock price
            volume: Trading volume
            market_cap: Market capitalization
        """
        self.symbol = symbol
        self.price = price
        self.volume = volume
        self.market_cap = market_cap
        self.client = anthropic.Anthropic()

    def analyze(self) -> str:
        """Analyze market data using Claude API with streaming.
        
        Returns:
            Analysis text from Claude
        """
        prompt = f"""Analyze the following market data and provide insights:
        
Stock Symbol: {self.symbol}
Current Price: ${self.price}
Trading Volume: {self.volume:,}
Market Cap: ${self.market_cap:,.0f}

Please provide:
1. A brief market assessment
2. Key observations about the trading metrics
3. Potential investment considerations
4. Risk factors to consider"""

        analysis = ""
        with self.client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        ) as stream:
            for text in stream.text_stream:
                analysis += text

        return analysis

    def get_data(self) -> dict:
        """Get market data as dictionary.
        
        Returns:
            Dictionary containing market data
        """
        return {
            "symbol": self.symbol,
            "price": self.price,
            "volume": self.volume,
            "market_cap": self.market_cap
        }

    def __str__(self) -> str:
        """String representation of market data."""
        return f"MarketData({self.symbol}: ${self.price}, Vol: {self.volume:,}, Cap: ${self.market_cap:,.0f})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"MarketData(symbol='{self.symbol}', price={self.price}, volume={self.volume}, market_cap={self.market_cap})"