class BaseConnectorManager:
    """Base class for connector managers."""

    def __init__(self, connector_class, connector_config: dict):
        self.connector_class = connector_class
        self.connector_config = connector_config

    def get_connection(self):
        connection = self._create_connection()
        if self._check_connection_health(connection):
            return connection
        else:
            self._close_connection(connection)
            return None

    def release_connection(self, connection):
        self._close_connection(connection)

    def shutdown(self):
        pass

    def _create_connection(self):
        return self.connector_class(**self.connector_config)

    def _check_connection_health(self, connection) -> bool:
        return True  # Placeholder for actual health check logic

    def _close_connection(self, connection):
        connection.close()  # Assuming the connection object has a close method