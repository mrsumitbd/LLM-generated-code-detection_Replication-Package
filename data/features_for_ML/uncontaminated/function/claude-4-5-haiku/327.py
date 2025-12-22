import anthropic
import json


def _select_choice(choices, rls_data):
    """
    Use Claude to select the best choice from a list based on RLS data.
    
    Args:
        choices: List of choices to select from
        rls_data: Data about RLS (Restless Leg Syndrome) or other context
    
    Returns:
        The selected choice from the list
    """
    client = anthropic.Anthropic()
    
    prompt = f"""Given the following choices and context data, select the best choice.

Choices:
{json.dumps(choices, indent=2)}

Context Data:
{json.dumps(rls_data, indent=2)}

Please analyze the choices based on the context data and return ONLY the selected choice as a plain string, without any explanation or additional text."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    selected = message.content[0].text.strip()
    
    if selected in choices:
        return selected
    
    for choice in choices:
        if choice.lower() in selected.lower() or selected.lower() in choice.lower():
            return choice
    
    return choices[0] if choices else None