from typing import Callable, TypeVar, ParamSpec, get_type_hints
import inspect
import json

P = ParamSpec('P')
R = TypeVar('R')

def llm_function(func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator to expose a method to the LLM (Language Learning Model) by capturing and storing its metadata.
    """
    
    # Get function signature and type hints
    sig = inspect.signature(func)
    type_hints = get_type_hints(func) if func.__annotations__ else {}
    
    # Extract docstring
    docstring = inspect.getdoc(func) or ""
    description = docstring.split('\n')[0] if docstring else ""
    
    # Parse docstring for parameter descriptions
    param_descriptions = {}
    if docstring:
        lines = docstring.split('\n')
        in_args = False
        for i, line in enumerate(lines):
            if 'Args:' in line:
                in_args = True
                continue
            if in_args:
                if line.strip().startswith('Returns:') or line.strip().startswith('Raises:'):
                    break
                if ':' in line and '(' in line:
                    # Parse "param_name (type): description"
                    parts = line.split(':')
                    if len(parts) >= 2:
                        param_part = parts[0].strip()
                        param_name = param_part.split('(')[0].strip()
                        desc = ':'.join(parts[1:]).strip()
                        param_descriptions[param_name] = desc
    
    # Build parameters schema
    properties = {}
    required = []
    
    for param_name, param in sig.parameters.items():
        if param_name == 'self' or param_name == 'cls':
            continue
        
        # Determine type
        param_type = type_hints.get(param_name, param.annotation)
        json_type = _python_type_to_json_schema(param_type)
        
        # Build property
        prop = {"type": json_type}
        
        # Add description if available
        if param_name in param_descriptions:
            prop["description"] = param_descriptions[param_name]
        
        properties[param_name] = prop
        
        # Check if required (no default value)
        if param.default == inspect.Parameter.empty:
            required.append(param_name)
    
    # Create ParametersSchema
    parameters_schema = {
        "type": "object",
        "properties": properties,
        "required": required
    }
    
    # Create FunctionSpec
    function_spec = {
        "name": func.__name__,
        "description": description,
        "parameters": parameters_schema
    }
    
    # Attach to function
    func._function_spec = function_spec
    
    return func


def _python_type_to_json_schema(python_type) -> str:
    """Convert Python type to JSON Schema type string."""
    if python_type == inspect.Parameter.empty:
        return "string"
    
    type_name = getattr(python_type, '__name__', str(python_type))
    
    type_mapping = {
        'int': 'integer',
        'float': 'number',
        'str': 'string',
        'bool': 'boolean',
        'list': 'array',
        'dict': 'object',
        'NoneType': 'null',
    }
    
    return type_mapping.get(type_name, 'string')