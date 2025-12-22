def _find_collection_response(op: Operation) -> Tuple[int, Any]:
    """
    Walks through defined operation responses and finds the first
    that is of a collection type (e.g. List[SomeSchema])
    """
    from typing import get_origin, get_args
    
    for status_code, response in op.responses.items():
        if response is None:
            continue
        
        # Get the response schema
        schema = response
        if hasattr(response, 'schema'):
            schema = response.schema
        
        # Check if it's a collection type
        origin = get_origin(schema)
        if origin is list:
            return (int(status_code), schema)
        
        # Check for typing.List or list annotation
        if hasattr(schema, '__origin__'):
            if schema.__origin__ is list:
                return (int(status_code), schema)
        
        # Check string representation for List
        schema_str = str(schema)
        if schema_str.startswith('typing.List') or schema_str.startswith('list['):
            return (int(status_code), schema)
    
    return (None, None)