class VectorStoreConfig:
    """Configuration for vector store connection."""

    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database = database

    @property
    def dsn(self) -> str:
        return f"host={self._host} port={self._port} user={self._user} password={self._password} dbname={self._database}"