import anthropic
import json
import os
from dataclasses import dataclass, field, asdict


@dataclass
class EventCfg:
    """Configuration for events."""
    
    name: str = ""
    description: str = ""
    enabled: bool = True
    retry_count: int = 3
    timeout_seconds: int = 30
    tags: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert configuration to JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: dict) -> "EventCfg":
        """Create configuration from dictionary."""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> "EventCfg":
        """Create configuration from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def validate(self) -> bool:
        """Validate the configuration."""
        if not self.name:
            return False
        if self.retry_count < 0:
            return False
        if self.timeout_seconds <= 0:
            return False
        return True
    
    def get_config_summary(self) -> str:
        """Get a summary of the configuration using Claude."""
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        
        config_str = self.to_json()
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Provide a brief summary of this event configuration:\n{config_str}"
                }
            ]
        )
        
        return message.content[0].text
    
    def __repr__(self) -> str:
        """String representation of the configuration."""
        return f"EventCfg(name={self.name!r}, enabled={self.enabled}, retry_count={self.retry_count}, timeout_seconds={self.timeout_seconds})"


if __name__ == "__main__":
    cfg = EventCfg(
        name="user_signup",
        description="Event triggered when a new user signs up",
        enabled=True,
        retry_count=3,
        timeout_seconds=30,
        tags=["user", "signup"],
        metadata={"version": "1.0", "priority": "high"}
    )
    
    print("Configuration:", cfg)
    print("Valid:", cfg.validate())
    print("JSON:", cfg.to_json())
    print("\nSummary from Claude:")
    print(cfg.get_config_summary())