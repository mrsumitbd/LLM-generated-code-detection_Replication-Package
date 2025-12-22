import anthropic
import json
from functools import wraps


def cgc_gff_option(func):
    """Decorator that adds Claude as a tool option to a function."""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if 'use_claude' is in kwargs
        use_claude = kwargs.pop('use_claude', False)
        
        if use_claude:
            # Use Claude to help with the function
            client = anthropic.Anthropic()
            
            # Get function name and docstring for context
            func_name = func.__name__
            func_doc = func.__doc__ or "No description available"
            
            # Create a prompt for Claude
            prompt = f"""You are helping to execute a function call. 
Function name: {func_name}
Function description: {func_doc}
Arguments: {json.dumps({'args': args, 'kwargs': kwargs}, default=str)}

Please provide a JSON response with the result of executing this function with the given arguments."""
            
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract the response
            response_text = message.content[0].text
            
            # Try to parse as JSON, otherwise return as string
            try:
                result = json.loads(response_text)
                return result
            except json.JSONDecodeError:
                return response_text
        else:
            # Execute the function normally
            return func(*args, **kwargs)
    
    return wrapper