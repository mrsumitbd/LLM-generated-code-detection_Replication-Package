import anthropic


def get_continuous_action(d_acts, c_act_max, c_act_min, n_bins):
    """
    Convert discrete action indices to continuous action values using Claude.
    
    Args:
        d_acts: List of discrete action indices
        c_act_max: Maximum continuous action value
        c_act_min: Minimum continuous action value
        n_bins: Number of bins for discretization
    
    Returns:
        List of continuous action values
    """
    client = anthropic.Anthropic()
    
    prompt = f"""Given discrete action indices, convert them to continuous action values.

Parameters:
- Discrete action indices: {d_acts}
- Continuous action max: {c_act_max}
- Continuous action min: {c_act_min}
- Number of bins: {n_bins}

The conversion should map discrete indices (0 to n_bins-1) linearly to the continuous range [c_act_min, c_act_max].

For each discrete action index, calculate the corresponding continuous value using linear interpolation:
continuous_value = c_act_min + (index / (n_bins - 1)) * (c_act_max - c_act_min)

Return ONLY a Python list of the continuous action values, nothing else. Example format: [0.5, 1.2, -0.3]"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text.strip()
    continuous_actions = eval(response_text)
    
    return continuous_actions