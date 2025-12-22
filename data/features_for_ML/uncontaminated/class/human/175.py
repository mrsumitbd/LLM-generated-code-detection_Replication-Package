
class BaseConnectorManager:
    """Base class for connector managers."""

    def __init__(self, connector_class, connector_config: dict):
        """
        Initialize the connector manager.
        Args:
            connector_class: The class to instantiate for connections
            connector_config: Configuration for the connector
        """
        self.connector_class = connector_class
        self.connector_config = connector_config

    def get_connection(self):
        """Get a connection."""
        raise NotImplementedError

    def release_connection(self, connection):
        """Release a connection."""
        raise NotImplementedError

    def shutdown(self):
        """Shut down the connector manager."""
        raise NotImplementedError

    def _create_connection(self):
        """
        Create a new connection instance.
        Returns:
            A new connection
        Raises:
            ConnectionError: If the connection cannot be created
        """
        try:
            connection = self.connector_class(**self.connector_config)
            return connection
        except Exception as e:
            raise ConnectionError(f"Failed to create connection: {e}") from e

    def _check_connection_health(self, connection) -> bool:
        """
        Check if a connection is healthy.
        Args:
            connection: The connection to check
        Returns:
            True if the connection is healthy, False otherwise
        """
        try:
            if hasattr(connection, "is_connected"):
                return connection.is_connected()
            elif hasattr(connection, "_check_connection"):
                connection._check_connection()
                return True
            return True  # Assume healthy if we can't check
        except Exception:
            return False

    def _close_connection(self, connection):
        """
        Close a connection.
        Args:
            connection: The connection to close
        """
        try:
            if hasattr(connection, "close"):
                connection.close()
            elif hasattr(connection, "disconnect"):
                connection.disconnect()
        except Exception as e:
            logger.warning(f"Error closing connection: {e}")