from typing import Optional

# The TSNode type is provided by the tree_sitter library.
# Import it only if available; otherwise, allow the function to be type‑checked
# with a forward reference.
try:
    from tree_sitter import Node as TSNode
except Exception:  # pragma: no cover
    TSNode = "TSNode"  # type: ignore


def find_first_child_by_field_name(node: TSNode, field_name: str) -> Optional[TSNode]:
    """
    Return the first child of *node* that has the given *field_name*.
    If no such child exists, return ``None``.
    """
    # The tree_sitter Node API provides a convenient helper.
    try:
        child = node.child_by_field_name(field_name)
        return child  # may be None if the field is absent
    except AttributeError:
        # Fallback for older or custom TSNode implementations.
        for i in range(node.child_count):
            child = node.child(i)
            # Some implementations expose the field name via a property.
            if getattr(child, "field_name", None) == field_name:
                return child
        return None