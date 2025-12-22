def check_analysis_performed(messages: List, lookback: int = 15) -> bool:
    """
    Check if any analysis tools were used in recent messages.
    
    Args:
        messages: List of conversation messages
        lookback: Number of recent messages to check
        
    Returns:
        True if analysis tools were used (read, ls, analyze_ml_performance)
    """
    analysis_tools = ['read', 'ls', 'analyze_ml_performance']
    recent_messages = messages[-lookback:]
    
    for message in recent_messages:
        for tool in analysis_tools:
            if tool in message.lower():
                return True
    
    return False