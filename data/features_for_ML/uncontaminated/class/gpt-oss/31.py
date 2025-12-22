class SCDynamicInputConfiguration:
    """Define defaults for dynamic configuration."""

    def __init__(self) -> None:
        # Default configuration values
        self.host: str = "localhost"
        self.port: int = 80
        self.use_ssl: bool = False
        self.timeout: int = 30  # seconds
        self.retries: int = 3
        self.headers: dict | None = None

    def update(self, **kwargs) -> None:
        """Update configuration values from keyword arguments."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def update_from_dict(self, config: dict) -> None:
        """Update configuration values from a dictionary."""
        for key, value in config.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self) -> dict:
        """Return the configuration as a dictionary."""
        return {
            "host": self.host,
            "port": self.port,
            "use_ssl": self.use_ssl,
            "timeout": self.timeout,
            "retries": self.retries,
            "headers": self.headers,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"host={self.host!r}, "
            f"port={self.port!r}, "
            f"use_ssl={self.use_ssl!r}, "
            f"timeout={self.timeout!r}, "
            f"retries={self.retries!r}, "
            f"headers={self.headers!r})"
        )