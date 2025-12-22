import anthropic
import json
import re


def parse_directory_structure(data: str) -> dict:
    """
    Parses the directory structure string and returns a dictionary where:
      - Keys: directory names
      - Values: count of files in that directory.
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Parse the following directory structure and return a JSON object where:
- Keys are directory names (without paths, just the directory name)
- Values are the count of files in that directory

Directory structure:
{data}

Return ONLY a valid JSON object, no other text. Example format:
{{"directory_name": 5, "another_dir": 3}}"""
            }
        ]
    )
    
    response_text = message.content[0].text
    
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group()
        result = json.loads(json_str)
        return result
    
    return {}