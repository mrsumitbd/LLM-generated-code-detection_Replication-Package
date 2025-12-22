import anthropic
import json


def rand_gumbel_like(x):
    """
    Generate random samples from a Gumbel distribution with the same shape as x.
    
    Uses Claude to help implement the Gumbel distribution sampling.
    """
    client = anthropic.Anthropic()
    
    # Get the shape of x
    shape = x.shape if hasattr(x, 'shape') else (len(x),) if hasattr(x, '__len__') else (1,)
    
    # Use Claude to generate the implementation
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Generate Python code to sample from a Gumbel distribution with shape {shape}.
                
The Gumbel distribution can be sampled using the formula:
G = -log(-log(U)) where U is uniform(0,1)

Return only the Python code that generates the samples, nothing else. The code should:
1. Import numpy as np
2. Generate uniform random samples
3. Apply the Gumbel transformation
4. Return the result as a numpy array with shape {shape}

Do not include any explanation, just the code."""
            }
        ]
    )
    
    # Extract the code from Claude's response
    code = message.content[0].text
    
    # Clean up the code if it has markdown formatting
    if code.startswith("```"):
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[6:]
    if code.endswith("```"):
        code = code[:-3]
    
    code = code.strip()
    
    # Execute the generated code
    namespace = {}
    exec(code, namespace)
    
    # The code should define a way to generate samples
    # We'll create the samples directly using the Gumbel formula
    import numpy as np
    
    # Generate uniform random samples
    u = np.random.uniform(0, 1, size=shape)
    
    # Apply Gumbel transformation: G = -log(-log(U))
    # Add small epsilon to avoid log(0)
    epsilon = 1e-20
    gumbel_samples = -np.log(-np.log(u + epsilon) + epsilon)
    
    return gumbel_samples


if __name__ == "__main__":
    import numpy as np
    
    # Test the function
    x = np.zeros((3, 4))
    result = rand_gumbel_like(x)
    print(f"Input shape: {x.shape}")
    print(f"Output shape: {result.shape}")
    print(f"Output:\n{result}")