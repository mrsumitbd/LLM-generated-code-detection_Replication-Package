def process_node(node: DOMBaseNode, depth: int) -> None:
    """
    Recursively process a DOM node, printing its structure with indentation.
    """
    indent = "  " * depth

    # Handle element nodes
    if hasattr(node, "tag"):
        print(f"{indent}<{node.tag}>")

    # Handle text nodes or nodes with a text attribute
    if hasattr(node, "text") and node.text:
        print(f"{indent}  {node.text}")

    # Recurse into child nodes if present
    if hasattr(node, "children"):
        for child in node.children:
            process_node(child, depth + 1)

    # Close element tags
    if hasattr(node, "tag"):
        print(f"{indent}</{node.tag}>")