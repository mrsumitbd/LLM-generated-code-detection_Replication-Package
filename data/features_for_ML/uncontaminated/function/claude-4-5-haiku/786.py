import anthropic
from datetime import datetime


def normalize_age_gender(dob, gen, current_date):
    """
    Normalize age and gender data using Claude API.
    
    Args:
        dob: Date of birth (string in various formats)
        gen: Gender (string in various formats)
        current_date: Current date for age calculation (string in YYYY-MM-DD format)
    
    Returns:
        Dictionary with normalized 'age' (int) and 'gender' (str: 'M', 'F', or 'Other')
    """
    client = anthropic.Anthropic()
    
    prompt = f"""You are a data normalization expert. Given the following information, normalize the age and gender data.

Date of Birth: {dob}
Gender: {gen}
Current Date: {current_date}

Please:
1. Calculate the age based on the date of birth and current date
2. Normalize the gender to one of: 'M' (Male), 'F' (Female), or 'Other'

Return ONLY a JSON object with exactly this format (no markdown, no extra text):
{{"age": <integer>, "gender": "<M|F|Other>"}}

If you cannot determine the age or gender, use null for that field."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=100,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text.strip()
    
    import json
    result = json.loads(response_text)
    
    if result.get("age") is None:
        result["age"] = None
    else:
        result["age"] = int(result["age"])
    
    if result.get("gender") is None:
        result["gender"] = None
    else:
        result["gender"] = str(result["gender"])
    
    return result


if __name__ == "__main__":
    test_cases = [
        ("1990-05-15", "Male", "2024-01-15"),
        ("15/05/1990", "F", "2024-01-15"),
        ("May 15, 1990", "female", "2024-01-15"),
        ("1985-12-25", "M", "2024-01-15"),
    ]
    
    for dob, gen, current_date in test_cases:
        result = normalize_age_gender(dob, gen, current_date)
        print(f"DOB: {dob}, Gender: {gen} -> Age: {result['age']}, Gender: {result['gender']}")