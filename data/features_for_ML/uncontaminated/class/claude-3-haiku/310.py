from pydantic import BaseSettings

class Config(BaseSettings):
    """Pydantic configuration."""

    app_name: str = "My App"
    database_url: str
    secret_key: str
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"