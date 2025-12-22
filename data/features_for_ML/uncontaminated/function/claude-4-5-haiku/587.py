def check_analysis_performed(messages: List, lookback: int = 15) -> bool:
    """
    Check if any analysis tools were used in recent messages.
    
    Args:
        messages: List of conversation messages
        lookback: Number of recent messages to check
        
    Returns:
        True if analysis tools were used (read, ls, analyze_ml_performance)
    """
    analysis_tools = {'read', 'ls', 'analyze_ml_performance'}
    
    # Get the last 'lookback' messages
    recent_messages = messages[-lookback:] if len(messages) > lookback else messages
    
    # Check if any analysis tools were used in recent messages
    for message in recent_messages:
        if isinstance(message, dict):
            # Check if message contains tool use
            if 'tool_use' in message:
                tool_use = message['tool_use']
                if isinstance(tool_use, dict) and tool_use.get('name') in analysis_tools:
                    return True
            
            # Check in content field
            if 'content' in message:
                content = message['content']
                if isinstance(content, str):
                    for tool in analysis_tools:
                        if tool in content:
                            return True
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            if item.get('type') == 'tool_use' and item.get('name') in analysis_tools:
                                return True
                            if isinstance(item.get('text'), str):
                                for tool in analysis_tools:
                                    if tool in item.get('text', ''):
                                        return True
    
    return False