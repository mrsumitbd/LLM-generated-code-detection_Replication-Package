def avg_out_degree(self):
    """
    Average out-degree (only for directed graphs).
    """
    # Ensure the graph is directed
    if not getattr(self, "directed", False):
        raise ValueError("Average out-degree is defined only for directed graphs.")

    # Retrieve the adjacency structure and vertex list
    adj = getattr(self, "adj", {})
    vertices = getattr(self, "vertices", list(adj.keys()))

    # If there are no vertices, the average is 0
    if not vertices:
        return 0.0

    # Compute total out-degree
    total_out = 0
    for v in vertices:
        # For missing entries, treat as zero out-degree
        neighbors = adj.get(v, [])
        total_out += len(neighbors)

    # Return the average
    return total_out / len(vertices)