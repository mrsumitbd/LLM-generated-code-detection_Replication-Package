import MetaTrader5 as mt5

def connect(connection):
    """
    Connect to the MetaTrader 5 terminal.
    Returns:
        bool: True if successful, False otherwise.
    Raises:
        ConnectionError: If connection fails.
    """
    try:
        if not mt5.initialize(connection):
            return False
        return True
    except Exception as e:
        raise ConnectionError(f"Failed to connect to MetaTrader 5: {e}")