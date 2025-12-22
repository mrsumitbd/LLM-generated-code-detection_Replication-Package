class Position:
    """Trading position information."""

    def __init__(self, symbol, shares, price, commission):
        self.symbol = symbol
        self.shares = shares
        self.price = price
        self.commission = commission
        self.realized_pnl = 0
        self.unrealized_pnl = 0

    def close(self, close_price):
        self.realized_pnl = (close_price - self.price) * self.shares - self.commission
        self.shares = 0

    def update(self, current_price):
        self.unrealized_pnl = (current_price - self.price) * self.shares