def verify(max_steps: int, state: AgentState) -> dict:
    """
    ReAct agent for environment verification through test command execution.
    
    Args:
        max_steps (int): Maximum number of verification steps allowed
        state (AgentState): Current agent state with setup results
        
    Returns:
        dict: Updated state with verification results and success status
    """
    success = True
    results = []
    
    for step in range(max_steps):
        try:
            result = state.execute_test_command()
            results.append(result)
            if not result.success:
                success = False
                break
        except Exception as e:
            success = False
            results.append({'error': str(e)})
            break
    
    return {
        'success': success,
        'results': results
    }