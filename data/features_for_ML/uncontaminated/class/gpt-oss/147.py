class Config:
    """Configuration constants."""
    DEBUG = False
    LOG_LEVEL = "INFO"
    DATABASE_URI = "sqlite:///app.db"
    API_ENDPOINT = "https://api.example.com"
    TIMEOUT = 30
    RETRY_ATTEMPTS = 3
    CACHE_ENABLED = True
    SECRET_KEY = "default-secret-key"