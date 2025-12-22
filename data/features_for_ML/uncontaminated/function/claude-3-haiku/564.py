def instantiate_network(config):
    import networkx as nx

    G = nx.Graph()

    for node in config['nodes']:
        G.add_node(node['id'], **node['attributes'])

    for link in config['links']:
        G.add_edge(link['source'], link['target'], **link['attributes'])

    return G