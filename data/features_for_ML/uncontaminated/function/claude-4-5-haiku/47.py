def get_argument_content(
    element: GraphQLObjectType | GraphQLField, directive_name: str, argument_name: str
) -> Any | None:
    """
    Extracts the comment from a GraphQL element (field or named type).

    Args:
        element (GraphQLNamedType | GraphQLField): The GraphQL element to extract the comment from.
        directive_name: The name of the directive whose arguments are to be extracted.
        argument_name: The name of the argument whose content is to be extracted.

    Returns:
        str | None: The comment if present, otherwise None.
    """
    if not hasattr(element, 'ast_node') or element.ast_node is None:
        return None
    
    ast_node = element.ast_node
    
    if not hasattr(ast_node, 'directives') or ast_node.directives is None:
        return None
    
    for directive in ast_node.directives:
        if directive.name.value == directive_name:
            if hasattr(directive, 'arguments') and directive.arguments:
                for argument in directive.arguments:
                    if argument.name.value == argument_name:
                        if hasattr(argument.value, 'value'):
                            return argument.value.value
                        return argument.value
    
    return None