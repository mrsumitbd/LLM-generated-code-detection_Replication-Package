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
    query = connection.query(mt5.OrderSendResult)
    
    # Apply filters based on argument rules
    if ticket is not None:
        query = query.filter(mt5.OrderSendResult.ticket == ticket)
    else:
        if symbol_name is not None:
            query = query.filter(mt5.OrderSendResult.symbol == symbol_name)
        elif group is not None:
            query = query.filter(mt5.OrderSendResult.group == group)
    
    # Apply optional filters
    if order_type is not None:
        if isinstance(order_type, str):
            order_type = OrderType[order_type].value
        elif isinstance(order_type, OrderType):
            order_type = order_type.value
        query = query.filter(mt5.OrderSendResult.type == order_type)
    
    if order_state is not None:
        if isinstance(order_state, str):
            order_state = OrderState[order_state].value
        elif isinstance(order_state, OrderState):
            order_state = order_state.value
        query = query.filter(mt5.OrderSendResult.state == order_state)
    
    if order_filling is not None:
        if isinstance(order_filling, str):
            order_filling = OrderFilling[order_filling].value
        elif isinstance(order_filling, OrderFilling):
            order_filling = order_filling.value
        query = query.filter(mt5.OrderSendResult.type_filling == order_filling)
    
    if order_lifetime is not None:
        if isinstance(order_lifetime, str):
            order_lifetime = OrderTime[order_lifetime].value
        elif isinstance(order_lifetime, OrderTime):
            order_lifetime = order_lifetime.value
        query = query.filter(mt5.OrderSendResult.type_time == order_lifetime)
    
    # Order by time descending
    query = query.order_by(mt5.OrderSendResult.time_setup.desc())
    
    # Convert to DataFrame
    results = query.all()
    
    if not results:
        return pd.DataFrame()
    
    df = pd.DataFrame([r.__dict__ for r in results])
    
    return df