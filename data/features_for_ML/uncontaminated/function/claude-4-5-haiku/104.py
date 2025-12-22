import anthropic


def apply_gate(x, gate, tr_gate=None, tr_token=None):
    """
    Apply a gate operation using Claude API with extended thinking.
    
    Args:
        x: Input value
        gate: Gate operation to apply
        tr_gate: Optional thinking gate parameter
        tr_token: Optional thinking token parameter
    
    Returns:
        Result of applying the gate operation
    """
    client = anthropic.Anthropic()
    
    # Build the prompt for Claude
    prompt = f"""Apply the following gate operation to the input value.

Input value: {x}
Gate operation: {gate}
"""
    
    if tr_gate is not None:
        prompt += f"Thinking gate parameter: {tr_gate}\n"
    if tr_token is not None:
        prompt += f"Thinking token parameter: {tr_token}\n"
    
    prompt += """
Please apply this gate operation and return the result. 
For common gates:
- NOT gate: inverts the input (0->1, 1->0)
- AND gate: requires two inputs, returns 1 only if both are 1
- OR gate: requires two inputs, returns 1 if at least one is 1
- XOR gate: requires two inputs, returns 1 if inputs differ
- NAND gate: NOT AND
- NOR gate: NOT OR

Return only the numerical result."""
    
    # Use extended thinking for more complex operations
    budget_tokens = 5000
    if tr_token is not None:
        budget_tokens = tr_token
    
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=16000,
        thinking={
            "type": "enabled",
            "budget_tokens": budget_tokens
        },
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    # Extract the result from the response
    result_text = ""
    for block in response.content:
        if block.type == "text":
            result_text = block.text
            break
    
    # Parse the result
    result_text = result_text.strip()
    
    # Try to extract a number from the result
    try:
        # Remove common text patterns and extract the number
        result_text = result_text.replace("Result:", "").replace("The result is", "").strip()
        
        # Try to parse as integer first
        if result_text.isdigit() or (result_text.startswith('-') and result_text[1:].isdigit()):
            return int(result_text)
        
        # Try to parse as float
        return float(result_text)
    except (ValueError, AttributeError):
        # If we can't parse as a number, return the text
        return result_text


if __name__ == "__main__":
    # Test the function
    result = apply_gate(1, "NOT gate")
    print(f"NOT gate applied to 1: {result}")
    
    result = apply_gate(1, "AND gate with 0")
    print(f"AND gate applied to 1 and 0: {result}")
    
    result = apply_gate(1, "OR gate with 0")
    print(f"OR gate applied to 1 and 0: {result}")