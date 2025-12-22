def validate_helper(variable_node: VariableNode, data_type: DataType, path: List[str]) -> None:
    if isinstance(variable_node, VariableNode):
        if variable_node.data_type != data_type:
            raise ValueError(f"Invalid data type at path: {'.'.join(path)}")
        if variable_node.is_array:
            for i, item in enumerate(variable_node.value):
                validate_helper(item, data_type.element_type, path + [str(i)])
        else:
            if not isinstance(variable_node.value, data_type.python_type):
                raise ValueError(f"Invalid value type at path: {'.'.join(path)}")
    else:
        raise ValueError(f"Expected VariableNode at path: {'.'.join(path)}")