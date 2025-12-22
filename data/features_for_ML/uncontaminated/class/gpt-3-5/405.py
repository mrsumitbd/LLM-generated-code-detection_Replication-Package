class MarketData:
    """Container for market data and analysis."""
    
    def __init__(self, symbol, price, volume):
        self.symbol = symbol
        self.price = price
        self.volume = volume
        
    def update_price(self, new_price):
        self.price = new_price
        
    def update_volume(self, new_volume):
        self.volume = new_volume
        
    def get_symbol(self):
        return self.symbol
    
    def get_price(self):
        return self.price
    
    def get_volume(self):
        return self.volume