import anthropic


def fluid_field_weights_gravity(value):
    """
    Uses Claude to calculate fluid field weights based on gravity using extended thinking.
    
    Args:
        value: A numeric value representing some fluid field parameter
        
    Returns:
        A dictionary containing the thinking process and the calculated weights
    """
    client = anthropic.Anthropic()
    
    prompt = f"""Given a fluid field parameter value of {value}, calculate the weights that would be applied 
    to different gravity components in a fluid dynamics simulation. Consider:
    1. How gravity affects fluid density distribution
    2. The relationship between the parameter value and gravitational influence
    3. Typical weight distributions in fluid field calculations
    
    Provide specific numerical weights for:
    - Vertical gravity component weight
    - Horizontal pressure gradient weight
    - Buoyancy effect weight
    - Stratification weight
    
    Return the weights as decimal values between 0 and 1."""
    
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=16000,
        thinking={
            "type": "enabled",
            "budget_tokens": 10000
        },
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    
    # Extract the thinking and response content
    thinking_content = ""
    response_content = ""
    
    for block in response.content:
        if block.type == "thinking":
            thinking_content = block.thinking
        elif block.type == "text":
            response_content = block.text
    
    # Parse the response to extract weights
    weights = {
        "input_value": value,
        "thinking_process": thinking_content,
        "response": response_content,
        "weights": {}
    }
    
    # Extract numerical weights from the response
    lines = response_content.split('\n')
    for line in lines:
        line = line.strip()
        if 'vertical' in line.lower() and 'gravity' in line.lower():
            # Try to extract the weight value
            parts = line.split(':')
            if len(parts) > 1:
                try:
                    weight_str = parts[-1].strip().split()[0]
                    weights["weights"]["vertical_gravity"] = float(weight_str)
                except (ValueError, IndexError):
                    weights["weights"]["vertical_gravity"] = 0.4
        elif 'horizontal' in line.lower() and 'pressure' in line.lower():
            parts = line.split(':')
            if len(parts) > 1:
                try:
                    weight_str = parts[-1].strip().split()[0]
                    weights["weights"]["horizontal_pressure"] = float(weight_str)
                except (ValueError, IndexError):
                    weights["weights"]["horizontal_pressure"] = 0.3
        elif 'buoyancy' in line.lower():
            parts = line.split(':')
            if len(parts) > 1:
                try:
                    weight_str = parts[-1].strip().split()[0]
                    weights["weights"]["buoyancy"] = float(weight_str)
                except (ValueError, IndexError):
                    weights["weights"]["buoyancy"] = 0.2
        elif 'stratification' in line.lower():
            parts = line.split(':')
            if len(parts) > 1:
                try:
                    weight_str = parts[-1].strip().split()[0]
                    weights["weights"]["stratification"] = float(weight_str)
                except (ValueError, IndexError):
                    weights["weights"]["stratification"] = 0.1
    
    # Set default weights if not found
    if not weights["weights"]:
        weights["weights"] = {
            "vertical_gravity": 0.4,
            "horizontal_pressure": 0.3,
            "buoyancy": 0.2,
            "stratification": 0.1
        }
    
    return weights


if __name__ == "__main__":
    result = fluid_field_weights_gravity(9.81)
    print("Fluid Field Weights Calculation Result:")
    print(f"Input Value: {result['input_value']}")
    print(f"\nThinking Process:\n{result['thinking_process']}")
    print(f"\nResponse:\n{result['response']}")
    print(f"\nCalculated Weights:")
    for weight_name, weight_value in result['weights'].items():
        print(f"  {weight_name}: {weight_value}")