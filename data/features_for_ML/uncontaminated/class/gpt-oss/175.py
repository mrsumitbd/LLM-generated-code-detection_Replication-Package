class BaseConnectorManager:
    """Base class for connector managers."""

    def __init__(self, connector_class, connector_config: dict):
        """
        Initialize the manager with a connector class and its configuration.

        :param connector_class: The class used to create new connections.
        :param connector_config: Dictionary of keyword arguments for the connector.
        """
        self._connector_class = connector_class
        self._connector_config = connector_config
        self._pool = []

    def get_connection(self):
        """
        Retrieve a healthy connection from the pool or create a new one.

        :return: A connection instance.
        """
        # Try to reuse an existing connection
        while self._pool:
            conn = self._pool.pop()
            if self._check_connection_health(conn):
                return conn
            # Connection is unhealthy; close it and continue
            self._close_connection(conn)

        # No reusable connection; create a new one
        return self._create_connection()

    def release_connection(self, connection):
        """
        Return a connection to the pool for future reuse.

        :param connection: The connection instance to release.
        """
        if connection is not None:
            self._pool.append(connection)

    def shutdown(self):
        """
        Close all connections in the pool and clear the pool.
        """
        while self._pool:
            conn = self._pool.pop()
            self._close_connection(conn)

    def _create_connection(self):
        """
        Instantiate a new connection using the provided class and config.

        :return: A new connection instance.
        """
        try:
            return self._connector_class(**self._connector_config)
        except Exception as exc:
            raise RuntimeError(f"Failed to create connection: {exc}") from exc

    def _check_connection_health(self, connection) -> bool:
        """
        Determine if a connection is healthy.

        The method attempts to call common health-check methods on the connection.
        If none are available, it assumes the connection is healthy.

        :param connection: The connection instance to check.
        :return: True if healthy, False otherwise.
        """
        if connection is None:
            return False

        # Common health-check patterns
        health_methods = ["is_alive", "ping", "health_check", "is_connected"]
        for method_name in health_methods:
            method = getattr(connection, method_name, None)
            if callable(method):
                try:
                    result = method()
                    # Interpret truthy values as healthy
                    return bool(result)
                except Exception:
                    return False

        # Fallback: assume healthy if no health method is defined
        return True

    def _close_connection(self, connection):
        """
        Close a connection if it provides a close method.

        :param connection: The connection instance to close.
        """
        if connection is None:
            return
        close_method = getattr(connection, "close", None)
        if callable(close_method):
            try:
                close_method()
            except Exception:
                # Ignore errors during close to avoid cascading failures
                pass