import anthropic


def fluid_fluid_particles_potential_radius(value):
    """
    Calculate the fluid-fluid particles potential radius using Claude API.
    
    Args:
        value: A numeric value representing some parameter for the calculation
        
    Returns:
        The calculated potential radius as a float
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Calculate the fluid-fluid particles potential radius for the given value: {value}

Please provide the calculation using standard fluid dynamics formulas. The potential radius is typically calculated based on particle interactions and intermolecular forces.

Return only the numeric result as a float value, nothing else."""
            }
        ]
    )
    
    result_text = message.content[0].text.strip()
    result = float(result_text)
    
    return result


if __name__ == "__main__":
    test_value = 2.5
    radius = fluid_fluid_particles_potential_radius(test_value)
    print(f"Potential radius for value {test_value}: {radius}")