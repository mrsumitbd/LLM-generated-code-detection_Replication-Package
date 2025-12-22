def validate_helper(variable_node: VariableNode, data_type: DataType, path: List[str]) -> None:
    if variable_node.data_type != data_type:
        raise ValueError(f"Data type mismatch at path {'.'.join(path)}")
    if variable_node.children:
        for key, child_node in variable_node.children.items():
            validate_helper(child_node, data_type, path + [key])