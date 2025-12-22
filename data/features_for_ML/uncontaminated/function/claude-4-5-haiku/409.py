def schema_command(args: Namespace) -> None:
    import json
    from typing import Any, Dict
    
    # Get the schema based on the command
    if hasattr(args, 'schema_type'):
        schema_type = args.schema_type
    else:
        schema_type = getattr(args, 'type', None)
    
    # Define schemas for different types
    schemas: Dict[str, Any] = {
        'user': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'name': {'type': 'string'},
                'email': {'type': 'string', 'format': 'email'},
                'age': {'type': 'integer', 'minimum': 0}
            },
            'required': ['id', 'name', 'email']
        },
        'product': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'name': {'type': 'string'},
                'price': {'type': 'number', 'minimum': 0},
                'description': {'type': 'string'}
            },
            'required': ['id', 'name', 'price']
        },
        'order': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'user_id': {'type': 'integer'},
                'items': {'type': 'array', 'items': {'type': 'object'}},
                'total': {'type': 'number', 'minimum': 0}
            },
            'required': ['id', 'user_id', 'items']
        }
    }
    
    if schema_type and schema_type in schemas:
        schema = schemas[schema_type]
        output = json.dumps(schema, indent=2)
        print(output)
    elif schema_type:
        print(f"Error: Unknown schema type '{schema_type}'")
    else:
        # Print all available schemas
        all_schemas = {key: value for key, value in schemas.items()}
        output = json.dumps(all_schemas, indent=2)
        print(output)