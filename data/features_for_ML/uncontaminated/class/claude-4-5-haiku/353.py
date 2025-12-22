import anthropic
import json
from datetime import datetime


class YuzuhaCinema4QuickAssistTriggerRecord:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.records = []

    def add_trigger_record(self, trigger_type: str, context: str, timestamp: str = None) -> dict:
        """Add a new trigger record with Claude's analysis."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()

        # Use Claude to analyze the trigger context
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""Analyze this cinema quick assist trigger and provide a structured response:
                    
Trigger Type: {trigger_type}
Context: {context}

Please provide:
1. A brief analysis of the trigger
2. Recommended quick assist actions (as a list)
3. Priority level (high/medium/low)
4. Estimated resolution time in minutes

Format your response as JSON.""",
                }
            ],
        )

        # Parse Claude's response
        response_text = message.content[0].text

        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                analysis = json.loads(json_str)
            else:
                analysis = {"raw_response": response_text}
        except json.JSONDecodeError:
            analysis = {"raw_response": response_text}

        # Create the record
        record = {
            "id": len(self.records) + 1,
            "trigger_type": trigger_type,
            "context": context,
            "timestamp": timestamp,
            "analysis": analysis,
            "status": "recorded",
        }

        self.records.append(record)
        return record

    def get_quick_assist_suggestion(self, trigger_type: str, context: str) -> str:
        """Get a quick assist suggestion from Claude for a given trigger."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=512,
            messages=[
                {
                    "role": "user",
                    "content": f"""As a cinema quick assist expert, provide a concise suggestion for:
                    
Trigger Type: {trigger_type}
Context: {context}

Provide only the most important action to take immediately.""",
                }
            ],
        )

        return message.content[0].text

    def get_all_records(self) -> list:
        """Get all recorded triggers."""
        return self.records

    def get_records_by_type(self, trigger_type: str) -> list:
        """Get records filtered by trigger type."""
        return [r for r in self.records if r["trigger_type"] == trigger_type]

    def get_record_by_id(self, record_id: int) -> dict:
        """Get a specific record by ID."""
        for record in self.records:
            if record["id"] == record_id:
                return record
        return None

    def clear_records(self) -> None:
        """Clear all records."""
        self.records = []

    def get_summary(self) -> dict:
        """Get a summary of all records."""
        if not self.records:
            return {"total_records": 0, "summary": "No records found"}

        trigger_types = {}
        for record in self.records:
            trigger_type = record["trigger_type"]
            trigger_types[trigger_type] = trigger_types.get(trigger_type, 0) + 1

        return {
            "total_records": len(self.records),
            "trigger_types": trigger_types,
            "latest_record": self.records[-1] if self.records else None,
        }