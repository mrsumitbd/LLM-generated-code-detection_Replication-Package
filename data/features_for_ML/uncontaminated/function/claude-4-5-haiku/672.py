import anthropic
import json
import re


def get_fixed_tool_calls_or_text_output(json_str, max_depth=5):
    """
    Attempts to fix malformed JSON and extract tool calls or text output.
    Uses Claude to help fix JSON if it's invalid.
    """
    if max_depth <= 0:
        return None
    
    # Try to parse the JSON as-is first
    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError:
        pass
    
    # Try common fixes
    fixed_json = json_str
    
    # Remove markdown code blocks if present
    if fixed_json.startswith("```"):
        fixed_json = re.sub(r"^```(?:json)?\n?", "", fixed_json)
        fixed_json = re.sub(r"\n?```$", "", fixed_json)
    
    # Try to parse after removing markdown
    try:
        data = json.loads(fixed_json)
        return data
    except json.JSONDecodeError:
        pass
    
    # Try to fix common JSON issues
    # Add missing closing braces/brackets
    open_braces = fixed_json.count('{') - fixed_json.count('}')
    open_brackets = fixed_json.count('[') - fixed_json.count(']')
    
    if open_braces > 0:
        fixed_json += '}' * open_braces
    if open_brackets > 0:
        fixed_json += ']' * open_brackets
    
    try:
        data = json.loads(fixed_json)
        return data
    except json.JSONDecodeError:
        pass
    
    # Use Claude to fix the JSON
    client = anthropic.Anthropic()
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""Please fix this malformed JSON and return ONLY the valid JSON, no explanation:

{json_str}

If this appears to be tool calls, return a JSON object with a "tool_calls" array.
If this appears to be text output, return a JSON object with a "text" field.
Return ONLY valid JSON, nothing else."""
                }
            ]
        )
        
        response_text = message.content[0].text
        
        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            response_text = re.sub(r"^```(?:json)?\n?", "", response_text)
            response_text = re.sub(r"\n?```$", "", response_text)
        
        try:
            data = json.loads(response_text)
            return data
        except json.JSONDecodeError:
            # If Claude's response is still not valid JSON, try one more recursive call
            if max_depth > 1:
                return get_fixed_tool_calls_or_text_output(response_text, max_depth - 1)
            return None
    except Exception:
        return None