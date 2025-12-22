from graphql import (
    FloatValueNode,
    GraphQLEnumType,
    GraphQLField,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLSchema,
    GraphQLUnionType,
    IntValueNode,
)
from typing import Any

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
    args = get_directive_arguments(element, directive_name)
    return args.get(argument_name) if args and argument_name in args else None