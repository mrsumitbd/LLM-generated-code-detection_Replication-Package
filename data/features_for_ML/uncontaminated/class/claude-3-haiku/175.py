import time
import threading

class BaseConnectorManager:
    """Base class for connector managers."""

    def __init__(self, connector_class, connector_config: dict):
        self._connector_class = connector_class
        self._connector_config = connector_config
        self._connections = []
        self._lock = threading.Lock()

    def get_connection(self):
        with self._lock:
            if self._connections:
                connection = self._connections.pop()
            else:
                connection = self._create_connection()
            return connection

    def release_connection(self, connection):
        with self._lock:
            if self._check_connection_health(connection):
                self._connections.append(connection)
            else:
                self._close_connection(connection)

    def shutdown(self):
        with self._lock:
            while self._connections:
                connection = self._connections.pop()
                self._close_connection(connection)

    def _create_connection(self):
        connection = self._connector_class(**self._connector_config)
        return connection

    def _check_connection_health(self, connection) -> bool:
        try:
            connection.ping()
            return True
        except Exception:
            return False

    def _close_connection(self, connection):
        connection.close()