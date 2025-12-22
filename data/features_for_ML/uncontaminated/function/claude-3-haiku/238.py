import pandas as pd
from typing import Optional, Union
from enum import Enum

class OrderType(Enum):
    MARKET = 'market'
    LIMIT = 'limit'
    STOP = 'stop'
    STOP_LIMIT = 'stop_limit'

class OrderState(Enum):
    PENDING = 'pending'
    OPENED = 'opened'
    CLOSED = 'closed'
    REJECTED = 'rejected'

class OrderFilling(Enum):
    FILL_OR_KILL = 'fill_or_kill'
    IMMEDIATE_OR_CANCEL = 'immediate_or_cancel'
    RETURN_PARTIAL = 'return_partial'

class OrderTime(Enum):
    GOOD_TILL_CANCEL = 'good_till_cancel'
    GOOD_TILL_DATE = 'good_till_date'
    GOOD_TILL_TIME = 'good_till_time'

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
    # Implement the function logic here
    query = "SELECT * FROM orders WHERE status = 'pending'"
    
    if ticket is not None:
        query += f" AND ticket = {ticket}"
    elif symbol_name is not None:
        query += f" AND symbol_name = '{symbol_name}'"
    elif group is not None:
        query += f" AND `group` = '{group}'"
    
    if order_type is not None:
        if isinstance(order_type, str):
            order_type = OrderType[order_type.upper()].value
        elif isinstance(order_type, int):
            order_type = OrderType(order_type).value
        query += f" AND type = '{order_type}'"
    
    if order_state is not None:
        if isinstance(order_state, str):
            order_state = OrderState[order_state.upper()].value
        elif isinstance(order_state, int):
            order_state = OrderState(order_state).value
        query += f" AND status = '{order_state}'"
    
    if order_filling is not None:
        if isinstance(order_filling, str):
            order_filling = OrderFilling[order_filling.upper()].value
        elif isinstance(order_filling, int):
            order_filling = OrderFilling(order_filling).value
        query += f" AND filling = '{order_filling}'"
    
    if order_lifetime is not None:
        if isinstance(order_lifetime, str):
            order_lifetime = OrderTime[order_lifetime.upper()].value
        elif isinstance(order_lifetime, int):
            order_lifetime = OrderTime(order_lifetime).value
        query += f" AND lifetime = '{order_lifetime}'"
    
    query += " ORDER BY time DESC"
    
    df = pd.read_sql_query(query, connection)
    return df