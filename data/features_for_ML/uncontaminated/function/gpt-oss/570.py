import MetaTrader5 as mt5

def connect(connection):
    """
    Connect to the MetaTrader 5 terminal.
    Returns:
        bool: True if successful, False otherwise.
    Raises:
        ConnectionError: If connection fails.
    """
    # Prepare initialization arguments
    init_kwargs = {}
    if isinstance(connection, dict):
        init_kwargs = connection

    try:
        # Attempt to initialize the MT5 terminal
        success = mt5.initialize(**init_kwargs)
        if not success:
            # MT5 initialization failed – raise an error with details
            raise ConnectionError(f"MT5 initialization failed: {mt5.last_error()}")
        return True
    except Exception as exc:
        # Wrap any exception in a ConnectionError
        raise ConnectionError(f"MT5 connection error: {exc}") from exc