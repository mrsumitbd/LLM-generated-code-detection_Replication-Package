import json as json_module
from typing import TypeVar, Union, get_args, get_origin
import anthropic

T = TypeVar('T')

def deserialize(value: str | bytes, target_type: type[T], json: bool = False) -> T:
    """
    Deserialize a value to a target type using Claude as an AI backbone.
    
    Args:
        value: The value to deserialize (string or bytes)
        target_type: The target type to deserialize to
        json: Whether to parse as JSON first
    
    Returns:
        The deserialized value of the target type
    """
    # Convert bytes to string if needed
    if isinstance(value, bytes):
        value = value.decode('utf-8')
    
    # If json flag is set, parse as JSON first
    if json:
        parsed_value = json_module.loads(value)
    else:
        parsed_value = value
    
    # Get the type name for the prompt
    if hasattr(target_type, '__name__'):
        type_name = target_type.__name__
    else:
        type_name = str(target_type)
    
    # Create a prompt for Claude to help with deserialization
    client = anthropic.Anthropic()
    
    prompt = f"""You are a Python deserialization expert. Convert the following value to a Python object of type {type_name}.

Value to deserialize:
{str(parsed_value)}

Target type: {type_name}

Return ONLY valid Python code that creates an instance of {type_name} from the given value. 
The code should be a single expression that can be evaluated with eval().
Do not include any explanation, markdown formatting, or code blocks - just the raw Python expression."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the response text
    response_text = message.content[0].text.strip()
    
    # Evaluate the response to get the deserialized object
    # Create a safe namespace with common types
    safe_dict = {
        'str': str,
        'int': int,
        'float': float,
        'bool': bool,
        'list': list,
        'dict': dict,
        'tuple': tuple,
        'set': set,
        'frozenset': frozenset,
        'bytes': bytes,
        'bytearray': bytearray,
        'complex': complex,
        'range': range,
        'slice': slice,
        'type': type,
        'object': object,
        'None': None,
        'True': True,
        'False': False,
    }
    
    # Add the target type to the namespace
    safe_dict[type_name] = target_type
    
    try:
        result = eval(response_text, {"__builtins__": {}}, safe_dict)
        return result
    except Exception as e:
        # If evaluation fails, try to return the parsed value directly
        # or convert it to the target type
        if target_type == str:
            return str(parsed_value)
        elif target_type == int:
            return int(parsed_value)
        elif target_type == float:
            return float(parsed_value)
        elif target_type == bool:
            return bool(parsed_value)
        elif target_type == list:
            if isinstance(parsed_value, list):
                return parsed_value
            return [parsed_value]
        elif target_type == dict:
            if isinstance(parsed_value, dict):
                return parsed_value
            return {}
        else:
            raise ValueError(f"Could not deserialize to {type_name}: {e}")