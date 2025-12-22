class Config:
    """Configuration constants."""

    # Database connection settings
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "myapp"
    DB_USER = "myuser"
    DB_PASSWORD = "mypassword"

    # Application settings
    APP_NAME = "My Application"
    APP_VERSION = "1.0.0"
    DEBUG = True
    LOG_LEVEL = "INFO"

    # Email settings
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = "myemail@example.com"
    SMTP_PASSWORD = "myemailpassword"
    DEFAULT_SENDER = "noreply@myapp.com"

    # Security settings
    SECRET_KEY = "my_super_secret_key"
    JWT_EXPIRATION_DAYS = 7

    # Third-party API keys
    GOOGLE_API_KEY = "my_google_api_key"
    TWITTER_API_KEY = "my_twitter_api_key"
    TWITTER_API_SECRET = "my_twitter_api_secret"