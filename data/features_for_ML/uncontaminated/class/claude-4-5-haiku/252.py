import anthropic
import json
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class BaseBuffRecord:
    """基础记录Class"""
    
    id: str = ""
    name: str = ""
    description: str = ""
    created_at: str = ""
    updated_at: str = ""
    metadata: dict = field(default_factory=dict)
    
    def __init__(self):
        self.id = ""
        self.name = ""
        self.description = ""
        self.created_at = ""
        self.updated_at = ""
        self.metadata = {}
    
    def to_dict(self) -> dict:
        """Convert record to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata
        }
    
    def from_dict(self, data: dict) -> None:
        """Load record from dictionary"""
        self.id = data.get("id", "")
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.created_at = data.get("created_at", "")
        self.updated_at = data.get("updated_at", "")
        self.metadata = data.get("metadata", {})
    
    def to_json(self) -> str:
        """Convert record to JSON string"""
        return json.dumps(self.to_dict())
    
    def from_json(self, json_str: str) -> None:
        """Load record from JSON string"""
        data = json.loads(json_str)
        self.from_dict(data)
    
    def __str__(self) -> str:
        """String representation"""
        return f"BaseBuffRecord(id={self.id}, name={self.name})"
    
    def __repr__(self) -> str:
        """Developer representation"""
        return self.__str__()


def demonstrate_buff_record():
    """Demonstrate the BaseBuffRecord class with Claude API"""
    
    client = anthropic.Anthropic()
    
    record = BaseBuffRecord()
    record.id = "buff_001"
    record.name = "Sample Buff Record"
    record.description = "This is a sample buff record for demonstration"
    record.created_at = "2024-01-01T00:00:00Z"
    record.updated_at = "2024-01-02T00:00:00Z"
    record.metadata = {"version": "1.0", "status": "active"}
    
    print("Created BaseBuffRecord:")
    print(f"  {record}")
    print(f"  Dict: {record.to_dict()}")
    print(f"  JSON: {record.to_json()}")
    
    json_data = record.to_json()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""I have a BaseBuffRecord with the following JSON data:
{json_data}

Please analyze this record and provide:
1. A summary of the record
2. Any observations about the metadata
3. Suggestions for how this record might be used in a system

Format your response as a structured analysis."""
            }
        ]
    )
    
    print("\nClaude's Analysis:")
    print(message.content[0].text)
    
    new_record = BaseBuffRecord()
    new_record.from_json(json_data)
    print("\nLoaded record from JSON:")
    print(f"  {new_record}")
    print(f"  Metadata: {new_record.metadata}")


if __name__ == "__main__":
    demonstrate_buff_record()