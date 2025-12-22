from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, Optional


class Position:
    """Trading position information."""

    def __init__(
        self,
        symbol: str,
        quantity: float,
        entry_price: float,
        entry_time: datetime,
        side: str = "long",
    ) -> None:
        if side.lower() not in {"long", "short"}:
            raise ValueError("side must be 'long' or 'short'")
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        self.symbol: str = symbol
        self.quantity: float = quantity
        self.entry_price: float = float(entry_price)
        self.entry_time: datetime = entry_time
        self.side: str = side.lower()
        self.current_price: float = self.entry_price
        self.current_time: datetime = entry_time
        self._realized_pnl: float = 0.0
        self._closed: bool = False

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def is_open(self) -> bool:
        """Return True if the position is still open."""
        return not self._closed

    @property
    def realized_pnl(self) -> float:
        """Return the realized profit/loss."""
        return self._realized_pnl

    @property
    def unrealized_pnl(self) -> float:
        """Return the unrealized profit/loss."""
        if self._closed:
            return 0.0
        if self.side == "long":
            return (self.current_price - self.entry_price) * self.quantity
        return (self.entry_price - self.current_price) * self.quantity

    @property
    def current_value(self) -> float:
        """Return the current market value of the position."""
        return self.quantity * self.current_price

    @property
    def entry_value(self) -> float:
        """Return the entry market value of the position."""
        return self.quantity * self.entry_price

    @property
    def absolute_return(self) -> float:
        """Return the absolute return (current - entry)."""
        return self.current_value - self.entry_value

    @property
    def percent_return(self) -> Optional[float]:
        """Return the percent return (current / entry - 1)."""
        if self.entry_value == 0:
            return None
        return (self.current_value / self.entry_value) - 1

    @property
    def size(self) -> float:
        """Return the absolute size of the position."""
        return abs(self.quantity)

    @property
    def direction(self) -> str:
        """Return the direction of the position ('long' or 'short')."""
        return self.side

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------
    def update_price(self, price: float, time: datetime) -> None:
        """Update the current market price and time."""
        if self._closed:
            raise RuntimeError("Cannot update price of a closed position")
        self.current_price = float(price)
        self.current_time = time

    def close(self, price: float, time: datetime) -> float:
        """Close the position at the given price and time.

        Returns the realized profit/loss from the close.
        """
        if self._closed:
            raise RuntimeError("Position already closed")
        close_price = float(price)
        if self.side == "long":
            pnl = (close_price - self.entry_price) * self.quantity
        else:
            pnl = (self.entry_price - close_price) * self.quantity
        self._realized_pnl += pnl
        self.current_price = close_price
        self.current_time = time
        self.quantity = 0.0
        self._closed = True
        return pnl

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the position."""
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "entry_price": self.entry_price,
            "entry_time": self.entry_time.isoformat(),
            "side": self.side,
            "current_price": self.current_price,
            "current_time": self.current_time.isoformat(),
            "realized_pnl": self._realized_pnl,
            "unrealized_pnl": self.unrealized_pnl,
            "is_open": self.is_open,
        }

    # ------------------------------------------------------------------
    # Representation helpers
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"Position(symbol={self.symbol!r}, quantity={self.quantity}, "
            f"entry_price={self.entry_price}, side={self.side!r}, "
            f"current_price={self.current_price}, is_open={self.is_open})"
        )

    def __str__(self) -> str:
        return (
            f"{self.symbol} ({self.side}) - Qty: {self.quantity} @ "
            f"{self.entry_price:.2f} (Current: {self.current_price:.2f})"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Position):
            return NotImplemented
        return (
            self.symbol == other.symbol
            and self.quantity == other.quantity
            and self.entry_price == other.entry_price
            and self.entry_time == other.entry_time
            and self.side == other.side
            and self.current_price == other.current_price
            and self.current_time == other.current_time
            and self._realized_pnl == other._realized_pnl
            and self._closed == other._closed
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.symbol,
                self.quantity,
                self.entry_price,
                self.entry_time,
                self.side,
                self.current_price,
                self.current_time,
                self._realized_pnl,
                self._closed,
            )
        )