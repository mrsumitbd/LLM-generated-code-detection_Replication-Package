import anthropic
import json
from dataclasses import dataclass


@dataclass
class VivianDotTriggerRecord:
    """A record for tracking Vivian.dot trigger events and their analysis."""
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.records = []
    
    def add_trigger_event(self, event_name: str, event_data: dict) -> dict:
        """Add a trigger event and get Claude's analysis."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this trigger event for Vivian.dot system:\nEvent: {event_name}\nData: {json.dumps(event_data)}\n\nProvide a brief analysis of what this trigger means and any recommended actions."
                }
            ]
        )
        
        analysis = message.content[0].text
        record = {
            "event_name": event_name,
            "event_data": event_data,
            "analysis": analysis
        }
        self.records.append(record)
        return record
    
    def get_records(self) -> list:
        """Get all recorded trigger events."""
        return self.records
    
    def clear_records(self) -> None:
        """Clear all recorded trigger events."""
        self.records = []
    
    def get_summary(self) -> str:
        """Get a summary of all trigger events."""
        if not self.records:
            return "No trigger events recorded."
        
        records_text = json.dumps(self.records, indent=2)
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Provide a concise summary of these Vivian.dot trigger events:\n{records_text}"
                }
            ]
        )
        
        return message.content[0].text