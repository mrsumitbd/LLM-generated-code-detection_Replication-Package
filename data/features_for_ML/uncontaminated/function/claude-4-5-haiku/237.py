import anthropic
import json


def build_crit_dict(gates):
    """
    Build a dictionary of critical gates from a list of gates using Claude.
    
    Args:
        gates: A list of gate objects or gate information
        
    Returns:
        A dictionary mapping gate names to their criticality information
    """
    client = anthropic.Anthropic()
    
    # Convert gates to a string representation for Claude
    gates_str = json.dumps(gates) if isinstance(gates, (list, dict)) else str(gates)
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Analyze the following gates and build a criticality dictionary. 
For each gate, determine if it's critical based on factors like:
- Gate type (AND gates are more critical than OR gates)
- Position in the circuit (gates closer to outputs are more critical)
- Fan-out (gates with higher fan-out are more critical)

Gates data:
{gates_str}

Return a JSON dictionary where keys are gate names/identifiers and values are criticality scores (0-1, where 1 is most critical).
Only return the JSON dictionary, no other text."""
            }
        ]
    )
    
    # Parse the response
    response_text = message.content[0].text
    
    # Try to extract JSON from the response
    try:
        # Look for JSON in the response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            crit_dict = json.loads(json_str)
        else:
            crit_dict = json.loads(response_text)
    except json.JSONDecodeError:
        # If parsing fails, create a basic dictionary
        crit_dict = {}
        if isinstance(gates, list):
            for i, gate in enumerate(gates):
                gate_name = str(gate) if not isinstance(gate, dict) else gate.get('name', f'gate_{i}')
                crit_dict[gate_name] = 0.5
        elif isinstance(gates, dict):
            for gate_name in gates:
                crit_dict[gate_name] = 0.5
    
    return crit_dict


if __name__ == "__main__":
    # Test with sample gates
    sample_gates = [
        {"name": "AND1", "type": "AND", "fan_out": 3},
        {"name": "OR1", "type": "OR", "fan_out": 1},
        {"name": "AND2", "type": "AND", "fan_out": 5},
        {"name": "NOT1", "type": "NOT", "fan_out": 2}
    ]
    
    result = build_crit_dict(sample_gates)
    print("Criticality Dictionary:")
    print(json.dumps(result, indent=2))