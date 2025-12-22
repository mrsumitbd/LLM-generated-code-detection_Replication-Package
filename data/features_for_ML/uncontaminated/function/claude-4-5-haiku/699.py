import anthropic


def get_optimization_parameters():
    """
    Uses Claude to generate optimization parameters for a machine learning model.
    Returns a dictionary with the optimization parameters.
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": """Generate optimization parameters for a machine learning model. 
                Return the parameters as a Python dictionary with the following keys:
                - learning_rate: a float between 0.0001 and 0.1
                - batch_size: an integer between 16 and 256
                - epochs: an integer between 10 and 100
                - optimizer: a string (e.g., 'adam', 'sgd', 'rmsprop')
                - momentum: a float between 0.8 and 0.99
                - weight_decay: a float between 0.0 and 0.01
                
                Return ONLY the Python dictionary, no other text."""
            }
        ]
    )
    
    response_text = message.content[0].text
    params_dict = eval(response_text)
    
    return params_dict


if __name__ == "__main__":
    params = get_optimization_parameters()
    print("Optimization Parameters:")
    for key, value in params.items():
        print(f"  {key}: {value}")