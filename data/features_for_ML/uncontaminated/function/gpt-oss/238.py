import pandas as pd
from typing import Optional, Union

# Assume these enums are defined somewhere in the project
try:
    from .enums import OrderType, OrderState, OrderFilling, OrderTime
except Exception:
    # Fallback definitions for demonstration purposes
    from enum import Enum

    class OrderType(Enum):
        BUY = 0
        SELL = 1

    class OrderState(Enum):
        PENDING = 0
        FILLED = 1

    class OrderFilling(Enum):
        MARKET = 0
        LIMIT = 1

    class OrderTime(Enum):
        GTC = 0
        DAY = 1


def _to_enum(value, enum_cls):
    """Convert a value to an enum member."""
    if value is None:
        return None
    if isinstance(value, enum_cls):
        return value
    if isinstance(value, int):
        try:
            return enum_cls(value)
        except ValueError:
            raise ValueError(f"Invalid integer {value} for enum {enum_cls.__name__}")
    if isinstance(value, str):
        try:
            return enum_cls[value.upper()]
        except KeyError:
            # Try case-insensitive match
            for member in enum_cls:
                if member.name.lower() == value.lower():
                    return member
            raise ValueError(f"Invalid string '{value}' for enum {enum_cls.__name__}")
    raise TypeError(f"Unsupported type {type(value)} for enum conversion")


def get_pending_orders(
    connection,
    ticket: Optional[Union[int, str]] = None,
    symbol_name: Optional[str] = None,
    group: Optional[str] = None,
    order_type: Optional[Union[str, int, OrderType]] = None,
    order_state: Optional[Union[str, int, OrderState]] = None,
    order_filling: Optional[Union[str, int, OrderFilling]] = None,
    order_lifetime: Optional[Union[str, int, OrderTime]] = None,
) -> pd.DataFrame:
    """
    Get pending orders.

    Argument rules:
    - All arguments are optionals.
    - If "ticket" is defined, then "symbol_name" and "group" will be ignored.
    - If "symbol_name" is defined, then "group" will be ignored.

    Returns:
        Pending orders in Panda's DataFrame, ordered by time (descending).
    """
    # Retrieve raw orders from the connection
    raw_orders = connection.get_pending_orders()
    if not isinstance(raw_orders, list):
        raise ValueError("Connection.get_pending_orders() must return a list of order dicts")

    # Convert enums if provided
    order_type_enum = _to_enum(order_type, OrderType)
    order_state_enum = _to_enum(order_state, OrderState)
    order_filling_enum = _to_enum(order_filling, OrderFilling)
    order_lifetime_enum = _to_enum(order_lifetime, OrderTime)

    # Helper to compare enum values
    def _match_enum(order_value, enum_member):
        if enum_member is None:
            return True
        return order_value == enum_member.value

    # Filter orders
    filtered = []
    for order in raw_orders:
        # Ticket filter has highest priority
        if ticket is not None:
            if str(order.get("ticket")) != str(ticket):
                continue
        else:
            # Symbol filter
            if symbol_name is not None:
                if order.get("symbol") != symbol_name:
                    continue
            else:
                # Group filter
                if group is not None:
                    if order.get("group") != group:
                        continue

        # Order type filter
        if order_type_enum is not None:
            if not _match_enum(order.get("type"), order_type_enum):
                continue

        # Order state filter
        if order_state_enum is not None:
            if not _match_enum(order.get("state"), order_state_enum):
                continue

        # Order filling filter
        if order_filling_enum is not None:
            if not _match_enum(order.get("filling"), order_filling_enum):
                continue

        # Order lifetime filter
        if order_lifetime_enum is not None:
            if not _match_enum(order.get("lifetime"), order_lifetime_enum):
                continue

        filtered.append(order)

    # Convert to DataFrame
    df = pd.DataFrame(filtered)

    # If 'time' column exists, sort by it descending
    if "time" in df.columns:
        try:
            df["time"] = pd.to_datetime(df["time"])
        except Exception:
            pass
        df = df.sort_values(by="time", ascending=False)

    return df