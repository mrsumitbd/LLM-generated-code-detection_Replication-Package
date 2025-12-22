from typing import Optional, Union
import pandas as pd

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
    # Implementation goes here
    pass