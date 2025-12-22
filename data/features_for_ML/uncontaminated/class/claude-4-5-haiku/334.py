import anthropic
import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class WebhookEvent:
    """Standardized webhook event structure."""
    
    event_type: str
    timestamp: str
    source: str
    data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert webhook event to dictionary."""
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "source": self.source,
            "data": self.data,
            "metadata": self.metadata,
        }
    
    def to_json(self) -> str:
        """Convert webhook event to JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WebhookEvent":
        """Create webhook event from dictionary."""
        return cls(
            event_type=data.get("event_type", ""),
            timestamp=data.get("timestamp", ""),
            source=data.get("source", ""),
            data=data.get("data", {}),
            metadata=data.get("metadata", {}),
        )
    
    def analyze_with_claude(self, analysis_prompt: str = None) -> str:
        """Analyze the webhook event using Claude AI."""
        client = anthropic.Anthropic()
        
        if analysis_prompt is None:
            analysis_prompt = f"""Analyze the following webhook event and provide insights:
            
Event Type: {self.event_type}
Timestamp: {self.timestamp}
Source: {self.source}
Data: {json.dumps(self.data, indent=2)}
Metadata: {json.dumps(self.metadata, indent=2)}

Please provide a brief analysis of this event."""
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": analysis_prompt}
            ]
        )
        
        return message.content[0].text


def main():
    """Main function to demonstrate WebhookEvent usage."""
    event = WebhookEvent(
        event_type="user.created",
        timestamp="2024-01-15T10:30:00Z",
        source="auth_service",
        data={
            "user_id": "usr_123",
            "email": "user@example.com",
            "name": "John Doe"
        },
        metadata={
            "request_id": "req_456",
            "ip_address": "192.168.1.1"
        }
    )
    
    print("Webhook Event:")
    print(event.to_json())
    print("\n" + "="*50 + "\n")
    
    analysis = event.analyze_with_claude()
    print("Claude Analysis:")
    print(analysis)


if __name__ == "__main__":
    main()