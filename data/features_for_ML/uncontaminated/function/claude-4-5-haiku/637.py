import anthropic


def Topeol_opt_init(tp, tf):
    """
    Initialize topology optimization using Claude API.
    
    Args:
        tp: Topology parameters
        tf: Target function or fitness function
    
    Returns:
        Initialized topology optimization state
    """
    client = anthropic.Anthropic()
    
    # Create a prompt for Claude to help initialize topology optimization
    prompt = f"""You are an expert in topology optimization. 
    
Given the following parameters:
- Topology parameters (tp): {tp}
- Target/fitness function (tf): {tf}

Please provide a structured initialization plan for topology optimization that includes:
1. Initial design domain setup
2. Boundary conditions and constraints
3. Material properties initialization
4. Optimization algorithm parameters
5. Convergence criteria

Format your response as a Python dictionary that can be used to initialize the optimization process."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the response
    response_text = message.content[0].text
    
    # Parse the response to create initialization state
    init_state = {
        "topology_params": tp,
        "target_function": tf,
        "claude_guidance": response_text,
        "status": "initialized",
        "iteration": 0,
        "best_fitness": None,
        "history": []
    }
    
    return init_state