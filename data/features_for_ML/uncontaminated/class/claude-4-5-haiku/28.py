import anthropic
import json
import re


class JaneCoreSkillStrikeCritRateBonusRecord:
    """A class to manage Jane Core Skill Strike Critical Rate Bonus Records using Claude AI."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.records = []

    def add_record(self, skill_name: str, base_crit_rate: float, bonus_percentage: float) -> dict:
        """Add a new critical rate bonus record for a skill."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a game mechanics expert. I need to calculate and validate a critical rate bonus record.
                    
Skill Name: {skill_name}
Base Critical Rate: {base_crit_rate}%
Bonus Percentage: {bonus_percentage}%

Please calculate:
1. The final critical rate after applying the bonus
2. Validate if the values are reasonable for a game skill
3. Provide a brief analysis

Return your response as a JSON object with keys: final_crit_rate, is_valid, analysis""",
                }
            ],
        )

        response_text = message.content[0].text
        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = {
                "final_crit_rate": base_crit_rate * (1 + bonus_percentage / 100),
                "is_valid": True,
                "analysis": "Record created successfully",
            }

        record = {
            "skill_name": skill_name,
            "base_crit_rate": base_crit_rate,
            "bonus_percentage": bonus_percentage,
            "final_crit_rate": result.get("final_crit_rate", base_crit_rate * (1 + bonus_percentage / 100)),
            "is_valid": result.get("is_valid", True),
            "analysis": result.get("analysis", ""),
        }

        self.records.append(record)
        return record

    def get_record(self, skill_name: str) -> dict | None:
        """Retrieve a record by skill name."""
        for record in self.records:
            if record["skill_name"].lower() == skill_name.lower():
                return record
        return None

    def list_all_records(self) -> list:
        """List all records."""
        return self.records

    def update_record(self, skill_name: str, new_bonus_percentage: float) -> dict | None:
        """Update the bonus percentage for an existing skill."""
        record = self.get_record(skill_name)
        if record:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Update the critical rate bonus calculation:
                        
Skill Name: {skill_name}
Base Critical Rate: {record['base_crit_rate']}%
New Bonus Percentage: {new_bonus_percentage}%

Calculate the new final critical rate and provide validation.
Return as JSON with keys: final_crit_rate, is_valid, analysis""",
                    }
                ],
            )

            response_text = message.content[0].text
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = {
                    "final_crit_rate": record["base_crit_rate"] * (1 + new_bonus_percentage / 100),
                    "is_valid": True,
                    "analysis": "Record updated successfully",
                }

            record["bonus_percentage"] = new_bonus_percentage
            record["final_crit_rate"] = result.get(
                "final_crit_rate", record["base_crit_rate"] * (1 + new_bonus_percentage / 100)
            )
            record["is_valid"] = result.get("is_valid", True)
            record["analysis"] = result.get("analysis", "")

            return record
        return None

    def delete_record(self, skill_name: str) -> bool:
        """Delete a record by skill name."""
        for i, record in enumerate(self.records):
            if record["skill_name"].lower() == skill_name.lower():
                self.records.pop(i)
                return True
        return False

    def get_statistics(self) -> dict:
        """Get statistics about all records."""
        if not self.records:
            return {"total_records": 0, "average_crit_rate": 0, "max_crit_rate": 0, "min_crit_rate": 0}

        crit_rates = [record["final_crit_rate"] for record in self.records]
        return {
            "total_records": len(self.records),
            "average_crit_rate": sum(crit_rates) / len(crit_rates),
            "max_crit_rate": max(crit_rates),
            "min_crit_rate": min(crit_rates),
        }

    def analyze_skill_balance(self, skill_name: str) -> str:
        """Use Claude to analyze if a skill's critical rate bonus is balanced."""
        record = self.get_record(skill_name)
        if not record:
            return f"Skill '{skill_name}' not found."

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""As a game balance expert, analyze this skill's critical rate bonus:
                    
Skill: {record['skill_name']}
Base Critical Rate: {record['base_crit_rate']}%
Bonus: {record['bonus_percentage']}%
Final Critical Rate: {record['final_crit_rate']}%

Is this balanced? What are the implications? Provide recommendations.""",
                }
            ],
        )

        return message.content[0].text


if __name__ == "__main__":
    record_manager = JaneCoreSkillStrikeCritRateBonusRecord()

    print("Adding records...")
    record1 = record_manager.add_record("Fireball", 15.0, 25.0)
    print(f"Added: {record1}")

    record2 = record_manager.add_record("Ice Storm", 10.0, 40.0)
    print(f"Added: {record2}")

    record3 = record_manager.add_record("Lightning Strike", 20.0, 15.0)
    print(f"Added: {record3}")

    print("\nAll records:")
    for record in record_manager.list_all_records():
        print(record)

    print("\nStatistics:")
    stats = record_manager.get_statistics()
    print(stats)

    print("\nUpdating Fireball bonus...")
    updated = record_manager.update_record("Fireball", 35.0)
    print(f"Updated: {updated}")

    print("\nAnalyzing Fireball balance...")
    analysis = record_manager.analyze_skill_balance("Fireball")
    print(f"Analysis: {analysis}")

    print("\nDeleting Ice Storm...")
    deleted = record_manager.delete_record("Ice Storm")
    print(f"Deleted: {deleted}")

    print("\nFinal records:")
    for record in record_manager.list_all_records():
        print(record)