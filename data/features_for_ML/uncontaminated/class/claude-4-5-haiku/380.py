import anthropic
import json
from datetime import datetime


class SessionData:
    """Data entry for a terminal session."""

    def __init__(self, session_id: str, user_input: str, assistant_response: str):
        """Initialize a SessionData entry.
        
        Args:
            session_id: Unique identifier for the session
            user_input: The user's input/command
            assistant_response: The assistant's response
        """
        self.session_id = session_id
        self.user_input = user_input
        self.assistant_response = assistant_response
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert session data to dictionary format."""
        return {
            "session_id": self.session_id,
            "user_input": self.user_input,
            "assistant_response": self.assistant_response,
            "timestamp": self.timestamp
        }

    def to_json(self) -> str:
        """Convert session data to JSON string."""
        return json.dumps(self.to_dict())

    def __repr__(self) -> str:
        """String representation of SessionData."""
        return f"SessionData(session_id={self.session_id}, timestamp={self.timestamp})"


def main():
    """Main function to demonstrate SessionData usage with Claude API."""
    client = anthropic.Anthropic()
    
    session_id = "session_001"
    user_input = "What is the capital of France?"
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    
    assistant_response = message.content[0].text
    
    session_data = SessionData(
        session_id=session_id,
        user_input=user_input,
        assistant_response=assistant_response
    )
    
    print("Session Data Created:")
    print(session_data)
    print("\nSession Data as Dictionary:")
    print(session_data.to_dict())
    print("\nSession Data as JSON:")
    print(session_data.to_json())


if __name__ == "__main__":
    main()