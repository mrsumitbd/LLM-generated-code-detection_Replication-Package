from typing import Any, Optional, Union
from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLDirective,
    GraphQLArgument,
)

def get_argument_content(
    element: Union[GraphQLObjectType, GraphQLField],
    directive_name: str,
    argument_name: str,
) -> Optional[Any]:
    """
    Extracts the content of a directive argument from a GraphQL element.

    Args:
        element (GraphQLObjectType | GraphQLField): The GraphQL element to extract the argument from.
        directive_name: The name of the directive whose arguments are to be extracted.
        argument_name: The name of the argument whose content is to be extracted.

    Returns:
        Any | None: The argument value if present, otherwise None.
    """
    # Retrieve the list of directives applied to the element, if any.
    directives = getattr(element, "directives", None)
    if not directives:
        return None

    # Iterate over the directives to find the one with the matching name.
    for directive in directives:
        # In graphql-core, a directive instance is a GraphQLDirective.
        if not isinstance(directive, GraphQLDirective):
            continue
        if directive.name != directive_name:
            continue

        # Get the arguments dictionary from the directive.
        args = getattr(directive, "arguments", {})
        if not isinstance(args, dict):
            continue

        # Retrieve the specific argument.
        arg = args.get(argument_name)
        if arg is None:
            continue

        # If the argument is a GraphQLArgument, return its default value.
        if isinstance(arg, GraphQLArgument):
            return arg.default_value

        # Otherwise, return the argument value directly.
        return arg

    # If no matching directive or argument was found, return None.
    return None