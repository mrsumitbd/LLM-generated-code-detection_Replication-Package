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
    if hasattr(element, 'directives'):
        for directive in element.directives:
            if directive.name == directive_name:
                if argument_name in directive.arguments:
                    return directive.arguments[argument_name].value
    return None