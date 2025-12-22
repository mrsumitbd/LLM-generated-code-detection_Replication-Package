class VectorStoreConfig:
    """Configuration for vector store connection."""

    def __init__(
        self,
        host: str,
        port: int = 5432,
        database: str = "",
        user: str = "",
        password: str = "",
        sslmode: str = "prefer",
        scheme: str = "postgresql",
    ) -> None:
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.sslmode = sslmode
        self.scheme = scheme

    @property
    def dsn(self) -> str:
        """Return a DSN string for connecting to the vector store."""
        auth = ""
        if self.user:
            auth = self.user
            if self.password:
                auth += f":{self.password}"
            auth += "@"

        db_part = f"/{self.database}" if self.database else ""
        query = f"?sslmode={self.sslmode}" if self.sslmode else ""

        return f"{self.scheme}://{auth}{self.host}:{self.port}{db_part}{query}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"host={self.host!r}, port={self.port!r}, database={self.database!r}, "
            f"user={self.user!r}, password={'***' if self.password else None!r}, "
            f"sslmode={self.sslmode!r}, scheme={self.scheme!r})"
        )