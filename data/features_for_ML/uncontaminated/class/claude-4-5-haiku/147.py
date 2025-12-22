class Config:
    """Configuration constants."""
    
    # Database configuration
    DATABASE_URL = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask configuration
    DEBUG = False
    TESTING = False
    SECRET_KEY = "dev-secret-key-change-in-production"
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 3600
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    
    # Logging configuration
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # API configuration
    API_TIMEOUT = 30
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Cache configuration
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Security
    PASSWORD_MIN_LENGTH = 8
    MAX_LOGIN_ATTEMPTS = 5
    LOGIN_ATTEMPT_TIMEOUT = 900  # 15 minutes
    
    # Email configuration
    MAIL_SERVER = "localhost"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = "noreply@example.com"
    
    # File upload
    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
    
    # Timezone
    TIMEZONE = "UTC"
    
    # Feature flags
    ENABLE_REGISTRATION = True
    ENABLE_EMAIL_VERIFICATION = False
    ENABLE_TWO_FACTOR_AUTH = False