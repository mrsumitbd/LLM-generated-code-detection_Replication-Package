import anthropic
from datetime import datetime

def is_current_time_within_range(time_range_str: str):
    """
    Determines if the current time falls within a given time range string.
    Uses Claude to parse and interpret the time range.
    
    Args:
        time_range_str: A string describing a time range (e.g., "9am to 5pm", "14:00-18:00")
    
    Returns:
        bool: True if current time is within the range, False otherwise
    """
    client = anthropic.Anthropic()
    
    current_time = datetime.now()
    current_time_str = current_time.strftime("%H:%M:%S")
    current_date_str = current_time.strftime("%Y-%m-%d")
    
    prompt = f"""Given the current time {current_time_str} on {current_date_str}, determine if it falls within the time range: "{time_range_str}"

Please respond with ONLY "true" or "false" (lowercase, no quotes).

Consider:
- 24-hour and 12-hour time formats
- AM/PM indicators
- Various separators (-, to, through, etc.)
- Handle edge cases like midnight and noon
- If the range spans midnight (e.g., "11pm to 2am"), consider it as spanning across days

Respond with only true or false."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=10,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text.strip().lower()
    
    return response_text == "true"


if __name__ == "__main__":
    test_ranges = [
        "9am to 5pm",
        "14:00-18:00",
        "8:00 AM - 12:00 PM",
        "11pm to 2am",
        "00:00-23:59",
        "6am through 10pm"
    ]
    
    for time_range in test_ranges:
        result = is_current_time_within_range(time_range)
        print(f"Time range '{time_range}': {result}")