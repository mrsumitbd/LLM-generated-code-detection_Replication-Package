import anthropic


def choose_device(devices: list) -> dict | None:
    """
    Use Claude to choose the best device from a list based on specifications.
    
    Args:
        devices: A list of device dictionaries with specifications
        
    Returns:
        The best device dictionary or None if no devices provided
    """
    if not devices:
        return None
    
    client = anthropic.Anthropic()
    
    devices_str = "\n".join([f"{i+1}. {device}" for i, device in enumerate(devices)])
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Given the following list of devices, choose the best one based on overall value, performance, and specifications. Return ONLY the number (1, 2, 3, etc.) of the best device.

Devices:
{devices_str}

Return only the number of the best device (e.g., "1" or "2"), nothing else."""
            }
        ]
    )
    
    response_text = message.content[0].text.strip()
    
    try:
        device_index = int(response_text) - 1
        if 0 <= device_index < len(devices):
            return devices[device_index]
    except (ValueError, IndexError):
        pass
    
    return None