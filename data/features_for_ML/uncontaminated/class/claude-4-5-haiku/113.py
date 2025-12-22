class Position:
    """Trading position information."""
    
    def __init__(self, symbol: str, quantity: float, entry_price: float, current_price: float = None):
        """
        Initialize a trading position.
        
        Args:
            symbol: The trading symbol/ticker
            quantity: Number of units held
            entry_price: Price at which position was entered
            current_price: Current market price (optional)
        """
        self.symbol = symbol
        self.quantity = quantity
        self.entry_price = entry_price
        self.current_price = current_price if current_price is not None else entry_price
    
    def get_entry_value(self) -> float:
        """Calculate total value at entry."""
        return self.quantity * self.entry_price
    
    def get_current_value(self) -> float:
        """Calculate current total value."""
        return self.quantity * self.current_price
    
    def get_unrealized_pnl(self) -> float:
        """Calculate unrealized profit/loss."""
        return self.get_current_value() - self.get_entry_value()
    
    def get_unrealized_pnl_percentage(self) -> float:
        """Calculate unrealized profit/loss as percentage."""
        if self.get_entry_value() == 0:
            return 0.0
        return (self.get_unrealized_pnl() / self.get_entry_value()) * 100
    
    def update_price(self, new_price: float) -> None:
        """Update the current price of the position."""
        self.current_price = new_price
    
    def add_to_position(self, quantity: float, price: float) -> None:
        """Add more units to the position and update average entry price."""
        total_quantity = self.quantity + quantity
        if total_quantity != 0:
            self.entry_price = (self.get_entry_value() + quantity * price) / total_quantity
            self.quantity = total_quantity
    
    def reduce_position(self, quantity: float) -> float:
        """
        Reduce position size.
        
        Args:
            quantity: Number of units to remove
            
        Returns:
            Realized profit/loss from the reduction
        """
        if quantity > self.quantity:
            quantity = self.quantity
        
        realized_pnl = quantity * (self.current_price - self.entry_price)
        self.quantity -= quantity
        
        return realized_pnl
    
    def close_position(self) -> float:
        """
        Close the entire position.
        
        Returns:
            Total realized profit/loss
        """
        realized_pnl = self.get_unrealized_pnl()
        self.quantity = 0
        return realized_pnl
    
    def __repr__(self) -> str:
        """String representation of the position."""
        return (f"Position(symbol={self.symbol}, quantity={self.quantity}, "
                f"entry_price={self.entry_price}, current_price={self.current_price}, "
                f"unrealized_pnl={self.get_unrealized_pnl():.2f})")
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return (f"{self.symbol}: {self.quantity} units @ ${self.entry_price:.2f} "
                f"(current: ${self.current_price:.2f}, P&L: ${self.get_unrealized_pnl():.2f})")