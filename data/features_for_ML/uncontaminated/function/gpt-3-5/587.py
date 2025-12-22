def check_analysis_performed(messages: List, lookback: int = 15) -> bool:
    recent_messages = messages[-lookback:]
    analysis_tools = ['read', 'ls', 'analyze_ml_performance']
    
    for message in recent_messages:
        if any(tool in message for tool in analysis_tools):
            return True
    
    return False