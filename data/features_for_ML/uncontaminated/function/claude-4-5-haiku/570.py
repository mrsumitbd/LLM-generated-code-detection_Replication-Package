def connect(connection):
    """
    Connect to the MetaTrader 5 terminal.
    Returns:
        bool: True if successful, False otherwise.
    Raises:
        ConnectionError: If connection fails.
    """
    try:
        if connection is None:
            raise ConnectionError("Connection object cannot be None")
        
        if not hasattr(connection, 'connect'):
            raise ConnectionError("Connection object must have a 'connect' method")
        
        result = connection.connect()
        
        if result is False:
            raise ConnectionError("Failed to connect to MetaTrader 5 terminal")
        
        return True
    
    except AttributeError as e:
        raise ConnectionError(f"Invalid connection object: {str(e)}")
    except Exception as e:
        raise ConnectionError(f"Connection failed: {str(e)}")