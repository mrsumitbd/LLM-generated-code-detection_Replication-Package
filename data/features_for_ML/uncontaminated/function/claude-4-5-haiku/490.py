import anthropic


def convert_module_to_f16(l):
    """
    Convert primitive modules to float16.
    """
    client = anthropic.Anthropic()
    
    # Create a prompt that asks Claude to help convert modules to float16
    prompt = f"""Given the following list of modules or code: {l}

Please convert these modules/code to use float16 (half precision) data type. 
Return only the converted code without any explanation."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    # Example usage
    example_code = """
    import torch
    import torch.nn as nn
    
    class SimpleModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = nn.Linear(10, 5)
            self.relu = nn.ReLU()
        
        def forward(self, x):
            x = self.linear(x)
            x = self.relu(x)
            return x
    """
    
    result = convert_module_to_f16(example_code)
    print(result)