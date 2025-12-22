import anthropic


def filterset(illuminant,
              values=[0, 0, 0],
              edges=[510,495,605,590],
              transitions=[10,10,10,10],
              ):
    """
    Generate a filterset configuration using Claude API.
    
    Args:
        illuminant: The illuminant type/name
        values: RGB values [R, G, B]
        edges: Edge wavelengths [edge1, edge2, edge3, edge4]
        transitions: Transition widths [trans1, trans2, trans3, trans4]
    
    Returns:
        A dictionary containing the filterset configuration
    """
    client = anthropic.Anthropic()
    
    prompt = f"""Generate a filterset configuration with the following parameters:
- Illuminant: {illuminant}
- RGB Values: R={values[0]}, G={values[1]}, B={values[2]}
- Edge wavelengths: {edges}
- Transition widths: {transitions}

Please provide a detailed filterset configuration that includes:
1. Filter specifications for each color channel
2. Wavelength ranges for each filter
3. Transition characteristics
4. Any relevant optical properties

Format the response as a structured configuration."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text
    
    filterset_config = {
        "illuminant": illuminant,
        "values": values,
        "edges": edges,
        "transitions": transitions,
        "configuration": response_text,
        "model": "claude-3-5-sonnet-20241022"
    }
    
    return filterset_config


if __name__ == "__main__":
    result = filterset(
        illuminant="D65",
        values=[255, 128, 64],
        edges=[510, 495, 605, 590],
        transitions=[10, 10, 10, 10]
    )
    
    print("Filterset Configuration:")
    print(f"Illuminant: {result['illuminant']}")
    print(f"Values: {result['values']}")
    print(f"Edges: {result['edges']}")
    print(f"Transitions: {result['transitions']}")
    print(f"\nGenerated Configuration:\n{result['configuration']}")