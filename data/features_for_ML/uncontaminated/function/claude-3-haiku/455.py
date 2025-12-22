def process_node(node: DOMBaseNode, depth: int) -> None:
    print(" " * depth + node.tag_name)
    for child in node.children:
        process_node(child, depth + 1)