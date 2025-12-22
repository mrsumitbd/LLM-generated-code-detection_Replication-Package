import anthropic


def compute_connected_components(*args, **kwargs):
    """
    Compute connected components in a graph using Claude as an AI backbone.
    
    Args:
        *args: Positional arguments (graph representation)
        **kwargs: Keyword arguments (may include 'graph' key)
    
    Returns:
        List of connected components, where each component is a list of nodes
    """
    client = anthropic.Anthropic()
    
    # Extract graph from arguments
    graph = None
    if args:
        graph = args[0]
    elif 'graph' in kwargs:
        graph = kwargs['graph']
    else:
        return []
    
    # Prepare the prompt for Claude
    prompt = f"""Given the following graph represented as an adjacency list:
{graph}

Please compute the connected components of this graph. A connected component is a maximal set of vertices such that there is a path between every pair of vertices.

Return the result as a Python list of lists, where each inner list represents one connected component containing the node identifiers.

For example, if the graph has nodes [1, 2, 3, 4, 5] and edges [(1,2), (2,3), (4,5)], the connected components would be [[1, 2, 3], [4, 5]].

Only return the Python list, no other text."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse the response
    response_text = message.content[0].text.strip()
    
    # Evaluate the response as Python code
    try:
        result = eval(response_text)
        return result
    except Exception:
        # If evaluation fails, return empty list
        return []