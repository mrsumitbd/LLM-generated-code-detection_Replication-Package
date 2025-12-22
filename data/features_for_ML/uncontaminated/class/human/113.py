from decimal import Decimal

class Position:
    """Trading position information."""
    symbol: str
    quantity: int
    entry_price: Decimal
    current_price: Decimal
    unrealized_pnl: Decimal
    asset_type: AssetType