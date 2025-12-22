import json
import re
from anthropic import Anthropic

def gpt_personality_analysis(dialogs, client):
    """
    Analyzes conversations to extract structured personality traits, general user data, 
    and assistant-related knowledge.
    Returns: {"profile": str, "user_data": str, "assistant_knowledge": str}
    """
    
    # Format the dialogs into a readable conversation string
    conversation_text = ""
    for dialog in dialogs:
        if isinstance(dialog, dict):
            role = dialog.get("role", "unknown")
            content = dialog.get("content", "")
            conversation_text += f"{role}: {content}\n"
        else:
            conversation_text += str(dialog) + "\n"
    
    # Create a system prompt for personality analysis
    system_prompt = """You are an expert personality analyst and data extractor. 
    Your task is to analyze conversations and extract:
    1. Personality traits and profile information about the user
    2. General user data (preferences, interests, background)
    3. Assistant-related knowledge (what the assistant knows about the user)
    
    Provide your analysis in JSON format with three keys: "profile", "user_data", and "assistant_knowledge".
    Each value should be a detailed string describing the findings."""
    
    # Use the Anthropic client to analyze the conversation
    messages = [
        {
            "role": "user",
            "content": f"""Please analyze the following conversation and extract personality traits, user data, and assistant knowledge.

Conversation:
{conversation_text}

Provide your response as a JSON object with the following structure:
{{
    "profile": "detailed personality profile and traits",
    "user_data": "general user information, preferences, and interests",
    "assistant_knowledge": "what the assistant knows or should know about the user"
}}"""
        }
    ]
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        system=system_prompt,
        messages=messages
    )
    
    # Extract the response text
    response_text = response.content[0].text
    
    # Try to parse the JSON response
    try:
        # Find JSON in the response
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(response_text)
    except json.JSONDecodeError:
        # If JSON parsing fails, create a structured response from the text
        result = {
            "profile": response_text,
            "user_data": "",
            "assistant_knowledge": ""
        }
    
    # Ensure all required keys are present
    if "profile" not in result:
        result["profile"] = ""
    if "user_data" not in result:
        result["user_data"] = ""
    if "assistant_knowledge" not in result:
        result["assistant_knowledge"] = ""
    
    return result