import anthropic
import json
import re


def extract_request_content(message_text):
    """
    Extract request content from a message using Claude API.
    
    Args:
        message_text: The message text to extract request content from
        
    Returns:
        A dictionary containing the extracted request content
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Extract the request content from the following message. 
Return the result as a JSON object with the following fields:
- request_type: The type of request (e.g., 'question', 'command', 'information_request', etc.)
- main_topic: The main topic or subject of the request
- details: Any specific details or parameters mentioned
- urgency: The urgency level if mentioned (e.g., 'high', 'normal', 'low')
- action_required: What action is being requested

Message: {message_text}

Return only valid JSON, no additional text."""
            }
        ]
    )
    
    response_text = message.content[0].text
    
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group()
        result = json.loads(json_str)
    else:
        result = json.loads(response_text)
    
    return result


if __name__ == "__main__":
    test_message = "I need to schedule a meeting with the team for next Monday at 2 PM to discuss the Q4 project roadmap. This is urgent."
    result = extract_request_content(test_message)
    print("Extracted Request Content:")
    print(json.dumps(result, indent=2))