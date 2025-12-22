def process_node(node: DOMBaseNode, depth: int) -> None:
    if node is None:
        return
    
    # Process the current node
    print("  " * depth + f"Node: {node.name if hasattr(node, 'name') else type(node).__name__}")
    
    # Process attributes if they exist
    if hasattr(node, 'attributes') and node.attributes:
        for attr_name, attr_value in node.attributes.items():
            print("  " * (depth + 1) + f"@{attr_name}: {attr_value}")
    
    # Process text content if it exists
    if hasattr(node, 'text') and node.text and node.text.strip():
        print("  " * (depth + 1) + f"Text: {node.text.strip()}")
    
    # Recursively process child nodes
    if hasattr(node, 'children') and node.children:
        for child in node.children:
            process_node(child, depth + 1)