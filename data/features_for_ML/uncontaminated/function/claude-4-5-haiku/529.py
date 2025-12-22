def validate_helper(variable_node: VariableNode, data_type: DataType, path: List[str]) -> None:
    if data_type is None:
        raise ValidationError(f"Data type is None at path {'.'.join(path)}")
    
    if isinstance(data_type, PrimitiveType):
        if not isinstance(variable_node.value, data_type.python_type):
            raise ValidationError(
                f"Expected {data_type.python_type.__name__} at path {'.'.join(path)}, "
                f"got {type(variable_node.value).__name__}"
            )
    
    elif isinstance(data_type, ArrayType):
        if not isinstance(variable_node.value, list):
            raise ValidationError(
                f"Expected list at path {'.'.join(path)}, "
                f"got {type(variable_node.value).__name__}"
            )
        
        for i, item in enumerate(variable_node.value):
            item_node = VariableNode(item)
            validate_helper(item_node, data_type.element_type, path + [f"[{i}]"])
    
    elif isinstance(data_type, ObjectType):
        if not isinstance(variable_node.value, dict):
            raise ValidationError(
                f"Expected dict at path {'.'.join(path)}, "
                f"got {type(variable_node.value).__name__}"
            )
        
        for field_name, field_type in data_type.fields.items():
            if field_name not in variable_node.value:
                raise ValidationError(
                    f"Missing required field '{field_name}' at path {'.'.join(path)}"
                )
            
            field_node = VariableNode(variable_node.value[field_name])
            validate_helper(field_node, field_type, path + [field_name])
    
    elif isinstance(data_type, UnionType):
        valid = False
        last_error = None
        
        for union_type in data_type.types:
            try:
                validate_helper(variable_node, union_type, path)
                valid = True
                break
            except ValidationError as e:
                last_error = e
        
        if not valid:
            raise ValidationError(
                f"Value at path {'.'.join(path)} does not match any type in union. "
                f"Last error: {str(last_error)}"
            )