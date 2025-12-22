import anthropic
import json
from datetime import datetime


class TimeweaverApBonusRecord:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.records = []

    def add_record(self, character_name: str, bonus_type: str, amount: int, timestamp: str = None) -> dict:
        """Add a new AP bonus record."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        record = {
            "character_name": character_name,
            "bonus_type": bonus_type,
            "amount": amount,
            "timestamp": timestamp
        }
        self.records.append(record)
        return record

    def get_records(self, character_name: str = None) -> list:
        """Get records, optionally filtered by character name."""
        if character_name:
            return [r for r in self.records if r["character_name"] == character_name]
        return self.records

    def analyze_bonuses(self, character_name: str = None) -> str:
        """Use Claude to analyze AP bonuses for a character or all characters."""
        records_to_analyze = self.get_records(character_name)
        
        if not records_to_analyze:
            return "No records found to analyze."
        
        records_json = json.dumps(records_to_analyze, indent=2)
        
        prompt = f"""Analyze the following AP (Ability Points) bonus records and provide insights:

{records_json}

Please provide:
1. Total AP gained
2. Most common bonus type
3. Average bonus amount
4. Timeline analysis
5. Any recommendations for optimization"""
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text

    def get_summary(self, character_name: str = None) -> dict:
        """Get a summary of AP bonuses."""
        records_to_summarize = self.get_records(character_name)
        
        if not records_to_summarize:
            return {"total_records": 0, "total_ap": 0, "characters": []}
        
        total_ap = sum(r["amount"] for r in records_to_summarize)
        bonus_types = {}
        characters = set()
        
        for record in records_to_summarize:
            bonus_type = record["bonus_type"]
            bonus_types[bonus_type] = bonus_types.get(bonus_type, 0) + record["amount"]
            characters.add(record["character_name"])
        
        return {
            "total_records": len(records_to_summarize),
            "total_ap": total_ap,
            "bonus_types": bonus_types,
            "characters": list(characters),
            "average_bonus": total_ap / len(records_to_summarize) if records_to_summarize else 0
        }

    def generate_report(self, character_name: str = None) -> str:
        """Generate a detailed report using Claude."""
        summary = self.get_summary(character_name)
        records = self.get_records(character_name)
        
        if not records:
            return "No records available for report generation."
        
        prompt = f"""Generate a detailed AP Bonus Report based on the following data:

Summary:
{json.dumps(summary, indent=2)}

Recent Records (last 5):
{json.dumps(records[-5:], indent=2)}

Please create a professional report including:
1. Executive Summary
2. Key Metrics
3. Trends and Patterns
4. Performance Analysis
5. Recommendations"""
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text

    def clear_records(self) -> None:
        """Clear all records."""
        self.records = []

    def export_records(self) -> str:
        """Export records as JSON string."""
        return json.dumps(self.records, indent=2)

    def import_records(self, json_string: str) -> None:
        """Import records from JSON string."""
        self.records = json.loads(json_string)