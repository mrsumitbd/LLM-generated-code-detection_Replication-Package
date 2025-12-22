def compute_connected_components(*args, **kwargs):
    """
    Compute connected components of an undirected graph.

    Parameters
    ----------
    *args
        The graph can be provided in one of the following forms:
        1. A single adjacency dictionary: {node: [neighbors, ...], ...}
        2. A single list of edges: [(u, v), ...]
        3. Two separate iterables: nodes, edges
    **kwargs
        - nodes: iterable of all nodes (used when edges are provided without adjacency dict)
        - directed: bool (default False). If True, the graph is treated as directed
          and strongly connected components are returned (using Kosaraju's algorithm).
        - return_type: str, one of 'list', 'dict', 'id'. Default 'list'.
            * 'list'  -> list of sets, each set is a component
            * 'dict'  -> dict mapping node -> component id (int)
            * 'id'    -> list of component ids for each node in sorted order

    Returns
    -------
    components
        Depending on `return_type`:
        * 'list': list of sets of nodes
        * 'dict': dict mapping node -> component id
        * 'id': list of component ids corresponding to sorted nodes
    """
    # Helper to build adjacency dict
    def build_adj(nodes_iter, edges_iter):
        adj = {n: set() for n in nodes_iter}
        for u, v in edges_iter:
            adj.setdefault(u, set()).add(v)
            adj.setdefault(v, set()).add(u)
        return adj

    # Parse arguments
    nodes = kwargs.get('nodes')
    directed = kwargs.get('directed', False)
    return_type = kwargs.get('return_type', 'list')

    # Determine graph representation
    if len(args) == 1:
        arg = args[0]
        if isinstance(arg, dict):
            # adjacency dict
            adj = {k: set(v) for k, v in arg.items()}
            nodes = adj.keys()
        elif isinstance(arg, (list, tuple)):
            # could be edge list or list of nodes
            if all(isinstance(e, (list, tuple)) and len(e) == 2 for e in arg):
                # edge list
                edges = arg
                if nodes is None:
                    nodes = set()
                    for u, v in edges:
                        nodes.update([u, v])
                adj = build_adj(nodes, edges)
            else:
                # treat as nodes list
                nodes = arg
                adj = {n: set() for n in nodes}
        else:
            raise TypeError("Unsupported graph representation.")
    elif len(args) == 2:
        nodes_iter, edges_iter = args
        nodes = nodes_iter
        edges = edges_iter
        adj = build_adj(nodes, edges)
    else:
        raise TypeError("compute_connected_components expects 1 or 2 positional arguments.")

    # Ensure adjacency dict has all nodes
    for n in nodes:
        adj.setdefault(n, set())

    # Function for undirected components
    def undirected_components():
        visited = set()
        comps = []
        for n in nodes:
            if n not in visited:
                stack = [n]
                comp = set()
                while stack:
                    cur = stack.pop()
                    if cur in visited:
                        continue
                    visited.add(cur)
                    comp.add(cur)
                    stack.extend(adj[cur] - visited)
                comps.append(comp)
        return comps

    # Function for strongly connected components (Kosaraju)
    def strongly_connected_components():
        # First DFS to get order
        visited = set()
        order = []

        def dfs(u):
            visited.add(u)
            for v in adj[u]:
                if v not in visited:
                    dfs(v)
            order.append(u)

        for n in nodes:
            if n not in visited:
                dfs(n)

        # Reverse graph
        rev_adj = {n: set() for n in nodes}
        for u in nodes:
            for v in adj[u]:
                rev_adj[v].add(u)

        # Second DFS on reversed graph
        visited.clear()
        comps = []

        def rev_dfs(u, comp):
            visited.add(u)
            comp.add(u)
            for v in rev_adj[u]:
                if v not in visited:
                    rev_dfs(v, comp)

        for u in reversed(order):
            if u not in visited:
                comp = set()
                rev_dfs(u, comp)
                comps.append(comp)
        return comps

    # Compute components
    if directed:
        comps = strongly_connected_components()
    else:
        comps = undirected_components()

    # Prepare output
    if return_type == 'list':
        return comps
    elif return_type == 'dict':
        mapping = {}
        for idx, comp in enumerate(comps):
            for node in comp:
                mapping[node] = idx
        return mapping
    elif return_type == 'id':
        sorted_nodes = sorted(nodes)
        mapping = {}
        for idx, comp in enumerate(comps):
            for node in comp:
                mapping[node] = idx
        return [mapping[n] for n in sorted_nodes]
    else:
        raise ValueError(f"Unsupported return_type: {return_type}")