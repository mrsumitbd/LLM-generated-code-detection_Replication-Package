import anthropic
import json
from dataclasses import dataclass


@dataclass
class RequestLogEntry:
    """Container for request log information"""
    timestamp: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    stop_reason: str
    request_type: str


def log_request(client: anthropic.Anthropic, model: str, messages: list, system: str = None) -> RequestLogEntry:
    """Make a request and log it"""
    import time
    from datetime import datetime
    
    timestamp = datetime.now().isoformat()
    
    # Make the API request
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system or "You are a helpful assistant.",
        messages=messages
    )
    
    # Extract usage information
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    total_tokens = input_tokens + output_tokens
    stop_reason = response.stop_reason
    
    # Determine request type based on messages
    request_type = "conversation"
    if len(messages) == 1:
        request_type = "single_message"
    
    # Create and return the log entry
    entry = RequestLogEntry(
        timestamp=timestamp,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        stop_reason=stop_reason,
        request_type=request_type
    )
    
    return entry


def main():
    """Main function to demonstrate RequestLogEntry usage"""
    client = anthropic.Anthropic()
    
    # Test with a simple message
    messages = [
        {"role": "user", "content": "What is 2+2?"}
    ]
    
    entry = log_request(client, "claude-3-5-sonnet-20241022", messages)
    
    print("Request Log Entry:")
    print(f"  Timestamp: {entry.timestamp}")
    print(f"  Model: {entry.model}")
    print(f"  Input Tokens: {entry.input_tokens}")
    print(f"  Output Tokens: {entry.output_tokens}")
    print(f"  Total Tokens: {entry.total_tokens}")
    print(f"  Stop Reason: {entry.stop_reason}")
    print(f"  Request Type: {entry.request_type}")
    
    # Test with a multi-turn conversation
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you for asking!"},
        {"role": "user", "content": "What can you help me with?"}
    ]
    
    entry = log_request(client, "claude-3-5-sonnet-20241022", messages)
    
    print("\nSecond Request Log Entry:")
    print(f"  Timestamp: {entry.timestamp}")
    print(f"  Model: {entry.model}")
    print(f"  Input Tokens: {entry.input_tokens}")
    print(f"  Output Tokens: {entry.output_tokens}")
    print(f"  Total Tokens: {entry.total_tokens}")
    print(f"  Stop Reason: {entry.stop_reason}")
    print(f"  Request Type: {entry.request_type}")


if __name__ == "__main__":
    main()