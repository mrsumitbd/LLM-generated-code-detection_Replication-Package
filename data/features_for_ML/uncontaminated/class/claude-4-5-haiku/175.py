class BaseConnectorManager:
    """Base class for connector managers."""

    def __init__(self, connector_class, connector_config: dict):
        self.connector_class = connector_class
        self.connector_config = connector_config
        self.connections = []
        self.available_connections = []
        self.in_use_connections = set()

    def get_connection(self):
        connection = None
        
        if self.available_connections:
            connection = self.available_connections.pop()
        else:
            connection = self._create_connection()
        
        if connection and self._check_connection_health(connection):
            self.in_use_connections.add(id(connection))
            return connection
        elif connection:
            self._close_connection(connection)
            return self.get_connection()
        
        return None

    def release_connection(self, connection):
        if connection is None:
            return
        
        conn_id = id(connection)
        if conn_id in self.in_use_connections:
            self.in_use_connections.remove(conn_id)
        
        if self._check_connection_health(connection):
            self.available_connections.append(connection)
        else:
            self._close_connection(connection)

    def shutdown(self):
        for connection in self.available_connections:
            self._close_connection(connection)
        
        for connection in list(self.in_use_connections):
            self._close_connection(connection)
        
        self.connections.clear()
        self.available_connections.clear()
        self.in_use_connections.clear()

    def _create_connection(self):
        try:
            connection = self.connector_class(**self.connector_config)
            self.connections.append(connection)
            return connection
        except Exception:
            return None

    def _check_connection_health(self, connection) -> bool:
        try:
            if hasattr(connection, 'is_connected'):
                return connection.is_connected()
            elif hasattr(connection, 'ping'):
                connection.ping()
                return True
            return True
        except Exception:
            return False

    def _close_connection(self, connection):
        try:
            if hasattr(connection, 'close'):
                connection.close()
            elif hasattr(connection, 'disconnect'):
                connection.disconnect()
        except Exception:
            pass