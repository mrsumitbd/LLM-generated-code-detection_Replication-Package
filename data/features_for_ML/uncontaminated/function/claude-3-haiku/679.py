from collections import defaultdict

def compute_connected_components(*args, **kwargs):
    graph = kwargs.get('graph', None)
    if graph is None:
        raise ValueError("'graph' parameter is required")

    visited = set()
    components = []

    def dfs(node):
        visited.add(node)
        component = [node]
        for neighbor in graph[node]:
            if neighbor not in visited:
                component.extend(dfs(neighbor))
        return component

    for node in graph:
        if node not in visited:
            components.append(dfs(node))

    return components