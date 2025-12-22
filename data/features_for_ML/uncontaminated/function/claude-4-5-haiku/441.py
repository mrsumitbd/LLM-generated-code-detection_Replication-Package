import anthropic
import json
from typing import Any


def validate_custom_voltage(
    data: dict[str, Any], errors: dict[str, str]
) -> dict[str, str]:
    """Validate custom voltage settings."""
    client = anthropic.Anthropic()
    
    # Prepare the validation request for Claude
    validation_prompt = f"""You are a voltage validation expert. Validate the following custom voltage settings data and return validation errors if any.

Data to validate:
{json.dumps(data, indent=2)}

Existing errors:
{json.dumps(errors, indent=2)}

Please validate the following aspects:
1. Check if voltage values are within reasonable ranges (typically 0-1000V for most applications)
2. Check if voltage_min is less than voltage_max
3. Check if required fields are present (voltage_min, voltage_max, unit)
4. Check if unit is a valid voltage unit (V, mV, kV)
5. Check if tolerance is a valid percentage (0-100)
6. Check if frequency is within valid range (0-1000 Hz)

Return ONLY a JSON object with field names as keys and error messages as values. If no errors, return an empty JSON object {{}}.
Example format: {{"voltage_min": "Voltage minimum must be positive", "unit": "Invalid unit specified"}}"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": validation_prompt}
        ]
    )
    
    # Parse the response
    response_text = message.content[0].text
    
    # Extract JSON from the response
    try:
        # Try to find JSON in the response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            validation_errors = json.loads(json_str)
        else:
            validation_errors = {}
    except (json.JSONDecodeError, ValueError):
        validation_errors = {}
    
    # Merge with existing errors
    merged_errors = {**errors, **validation_errors}
    
    return merged_errors