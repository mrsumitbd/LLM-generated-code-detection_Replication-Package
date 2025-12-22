class Position:
    """Trading position information."""
    
    def __init__(self, symbol, quantity, entry_price):
        self.symbol = symbol
        self.quantity = quantity
        self.entry_price = entry_price
        
    def update_quantity(self, new_quantity):
        self.quantity = new_quantity
        
    def update_entry_price(self, new_entry_price):
        self.entry_price = new_entry_price
        
    def calculate_position_value(self):
        return self.quantity * self.entry_price
        
    def __str__(self):
        return f"Position: {self.symbol}, Quantity: {self.quantity}, Entry Price: {self.entry_price}"