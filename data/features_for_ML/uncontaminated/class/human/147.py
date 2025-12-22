
class Config:
    """Configuration constants."""

    # Service URLs
    MCP_SERVER_URL = "http://127.0.0.1:18888/"
    SPARK_HISTORY_URL = "http://localhost:18080/api/v1/applications"
    OLLAMA_URL = "http://localhost:11434"

    # Model settings
    DEFAULT_MODEL = "qwen3:1.7b"
    MODEL_OPTIONS = {
        "qwen3:0.6b": {"size": "522MB", "quality": "Basic", "speed": "Fast"},
        "qwen3:1.7b": {"size": "1.4GB", "quality": "Better", "speed": "Moderate"},
    }

    # Agent settings
    TIMEOUT = 30.0
    MAX_TOKENS = 2048
    TEMPERATURE = 0.1

    # Sample application IDs
    SAMPLE_APPS = [
        "spark-cc4d115f011443d787f03a71a476a745",
        "spark-bcec39f6201b42b9925124595baad260",
        "spark-110be3a8424d4a2789cb88134418217b",
    ]