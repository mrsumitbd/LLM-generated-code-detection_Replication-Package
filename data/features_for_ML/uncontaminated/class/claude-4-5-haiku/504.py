import anthropic
import json
from dataclasses import dataclass


@dataclass
class LogDetail:
    """Standardized log detail structure."""
    timestamp: str
    level: str
    message: str
    source: str
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> dict:
        """Convert LogDetail to dictionary."""
        return {
            "timestamp": self.timestamp,
            "level": self.level,
            "message": self.message,
            "source": self.source,
            "metadata": self.metadata
        }

    def to_json(self) -> str:
        """Convert LogDetail to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict) -> "LogDetail":
        """Create LogDetail from dictionary."""
        return cls(
            timestamp=data.get("timestamp", ""),
            level=data.get("level", ""),
            message=data.get("message", ""),
            source=data.get("source", ""),
            metadata=data.get("metadata", {})
        )

    @classmethod
    def from_json(cls, json_str: str) -> "LogDetail":
        """Create LogDetail from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __str__(self) -> str:
        """String representation of LogDetail."""
        return f"[{self.timestamp}] {self.level} - {self.source}: {self.message}"

    def __repr__(self) -> str:
        """Detailed representation of LogDetail."""
        return f"LogDetail(timestamp={self.timestamp!r}, level={self.level!r}, message={self.message!r}, source={self.source!r}, metadata={self.metadata!r})"


def analyze_logs_with_claude(logs: list[LogDetail]) -> str:
    """
    Analyze a list of LogDetail objects using Claude API.
    
    Args:
        logs: List of LogDetail objects to analyze
        
    Returns:
        Analysis result from Claude
    """
    client = anthropic.Anthropic()
    
    # Convert logs to a readable format for Claude
    logs_text = "\n".join([str(log) for log in logs])
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Please analyze the following logs and provide insights:\n\n{logs_text}"
            }
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    # Example usage
    log1 = LogDetail(
        timestamp="2024-01-15T10:30:00Z",
        level="ERROR",
        message="Database connection failed",
        source="database.py",
        metadata={"error_code": 500, "retry_count": 3}
    )
    
    log2 = LogDetail(
        timestamp="2024-01-15T10:31:00Z",
        level="INFO",
        message="Attempting reconnection",
        source="database.py",
        metadata={"attempt": 1}
    )
    
    log3 = LogDetail(
        timestamp="2024-01-15T10:32:00Z",
        level="INFO",
        message="Connection restored",
        source="database.py",
        metadata={"connection_time_ms": 250}
    )
    
    # Test basic functionality
    print("Log 1:", log1)
    print("Log 2:", log2)
    print("Log 3:", log3)
    
    # Test JSON conversion
    json_str = log1.to_json()
    print("\nJSON representation:", json_str)
    
    # Test from_json
    log_from_json = LogDetail.from_json(json_str)
    print("Reconstructed from JSON:", log_from_json)
    
    # Analyze logs with Claude
    logs = [log1, log2, log3]
    print("\n--- Claude Analysis ---")
    analysis = analyze_logs_with_claude(logs)
    print(analysis)