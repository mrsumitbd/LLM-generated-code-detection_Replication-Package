import json
import anthropic


def _extract_last_applied(resource: dict) -> dict | None:
    """
    Extract the last-applied-configuration from a Kubernetes resource.
    
    This function uses Claude to parse the kubectl.kubernetes.io/last-applied-configuration
    annotation from a Kubernetes resource and return it as a dictionary.
    
    Args:
        resource: A Kubernetes resource dictionary
        
    Returns:
        The parsed last-applied-configuration as a dict, or None if not found
    """
    client = anthropic.Anthropic()
    
    # Check if the resource has annotations with last-applied-configuration
    annotations = resource.get("metadata", {}).get("annotations", {})
    last_applied_str = annotations.get("kubectl.kubernetes.io/last-applied-configuration")
    
    if not last_applied_str:
        return None
    
    # Use Claude to parse the JSON string
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Parse this JSON string and return only the parsed JSON object. 
Do not include any explanation or markdown formatting, just the raw JSON:

{last_applied_str}"""
            }
        ]
    )
    
    # Extract the response text
    response_text = message.content[0].text
    
    # Parse the JSON response
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return None