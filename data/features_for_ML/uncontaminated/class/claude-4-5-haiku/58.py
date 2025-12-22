import anthropic
import json
from datetime import datetime


class AstraYaoQuickAssistManagerTriggerRecord:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.records = []
        self.conversation_history = []

    def add_record(self, trigger_type: str, description: str, metadata: dict = None) -> dict:
        """Add a new trigger record."""
        record = {
            "id": len(self.records) + 1,
            "timestamp": datetime.now().isoformat(),
            "trigger_type": trigger_type,
            "description": description,
            "metadata": metadata or {},
        }
        self.records.append(record)
        return record

    def get_records(self) -> list:
        """Get all trigger records."""
        return self.records

    def analyze_triggers(self, query: str) -> str:
        """Analyze triggers using Claude with multi-turn conversation."""
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": query})

        # Prepare context about current records
        records_context = json.dumps(self.records, indent=2)
        system_prompt = f"""You are an expert assistant for analyzing trigger records in the Astra Yao Quick Assist Manager system.
        
Current trigger records:
{records_context}

Analyze the user's query about these triggers and provide insights, patterns, or recommendations."""

        # Make API call with conversation history
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=self.conversation_history,
        )

        # Extract response text
        assistant_message = response.content[0].text

        # Add assistant response to conversation history
        self.conversation_history.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def get_conversation_history(self) -> list:
        """Get the conversation history."""
        return self.conversation_history

    def clear_conversation(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []

    def clear_records(self) -> None:
        """Clear all trigger records."""
        self.records = []


def main():
    # Create manager instance
    manager = AstraYaoQuickAssistManagerTriggerRecord()

    # Add some sample trigger records
    manager.add_record(
        "user_action",
        "User clicked on help button",
        {"button_id": "help_btn_001", "page": "dashboard"},
    )
    manager.add_record(
        "system_event",
        "System detected performance degradation",
        {"cpu_usage": 85, "memory_usage": 92},
    )
    manager.add_record(
        "error_event",
        "API timeout occurred",
        {"endpoint": "/api/data", "response_time": 5000},
    )
    manager.add_record(
        "user_action",
        "User requested quick assist",
        {"request_type": "general_help", "context": "dashboard"},
    )

    print("=== Astra Yao Quick Assist Manager Trigger Record ===\n")

    # Display records
    print("Current Trigger Records:")
    for record in manager.get_records():
        print(f"  ID: {record['id']}, Type: {record['trigger_type']}, Description: {record['description']}")
    print()

    # Multi-turn conversation with Claude
    print("=== Analysis Conversation ===\n")

    # First query
    query1 = "What types of triggers do we have in our system?"
    print(f"User: {query1}")
    response1 = manager.analyze_triggers(query1)
    print(f"Assistant: {response1}\n")

    # Second query (continuing conversation)
    query2 = "Which triggers seem to indicate system issues?"
    print(f"User: {query2}")
    response2 = manager.analyze_triggers(query2)
    print(f"Assistant: {response2}\n")

    # Third query (continuing conversation)
    query3 = "What recommendations would you make to improve our trigger system?"
    print(f"User: {query3}")
    response3 = manager.analyze_triggers(query3)
    print(f"Assistant: {response3}\n")

    # Display conversation history
    print("=== Conversation History ===")
    for i, msg in enumerate(manager.get_conversation_history(), 1):
        role = "User" if msg["role"] == "user" else "Assistant"
        print(f"{i}. {role}: {msg['content'][:100]}...")


if __name__ == "__main__":
    main()