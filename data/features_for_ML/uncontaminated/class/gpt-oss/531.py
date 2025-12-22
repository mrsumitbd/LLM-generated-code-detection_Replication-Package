import networkx as nx
from collections import defaultdict

class DEPIMPACT:
    """
    A simple dependency impact analysis tool.

    Parameters
    ----------
    graph : networkx.Graph
        The original graph.
    poi : hashable
        Point of interest node.
    node_to_score : dict
        Mapping from node to an initial score.
    used_method : str
        Method to use for impact calculation ('degree' or 'loss').
    score_method : str
        How to combine scores ('sum' or 'average').
    """

    def __init__(self, graph, poi, node_to_score, used_method='degree', score_method='sum'):
        self.graph = graph
        self.poi = poi
        self.node_to_score = node_to_score
        self.used_method = used_method
        self.score_method = score_method
        self.subgraph = None
        self.dependency_graph = None
        self.degree_scores = {}
        self.loss_scores = {}
        self.combined_scores = {}

    def run(self):
        """Run the full impact analysis pipeline."""
        self.n_hop_subgraph_nodes()
        self.gen_dependency_graph()
        if self.used_method == 'degree':
            self._cal_degree_score()
        elif self.used_method == 'loss':
            self._cal_loss_score(self.node_to_score)
        else:
            raise ValueError(f"Unsupported used_method: {self.used_method}")

        # Convert to DAG if possible
        dag_nodes = self._convert_DAG()

        # Combine scores if both are available
        if self.degree_scores and self.loss_scores:
            self._cal_degree_recon_score(self.degree_scores, self.loss_scores)

        # Return a dictionary of final scores
        return self.combined_scores or self.degree_scores or self.loss_scores

    def n_hop_subgraph_nodes(self, hops=2):
        """
        Determine nodes within `hops` distance from the point of interest.
        """
        lengths = nx.single_source_shortest_path_length(self.graph, self.poi, cutoff=hops)
        self.subgraph = self.graph.subgraph(lengths.keys()).copy()
        return self.subgraph

    def gen_dependency_graph(self):
        """
        Generate a dependency graph from the subgraph.
        For directed graphs, this is the same as the subgraph.
        For undirected graphs, we create a directed version by arbitrarily orienting edges.
        """
        if self.subgraph is None:
            raise RuntimeError("Subgraph not initialized. Call n_hop_subgraph_nodes first.")
        if self.subgraph.is_directed():
            self.dependency_graph = self.subgraph.copy()
        else:
            # Arbitrary orientation: edge (u, v) becomes u -> v if u < v
            dg = nx.DiGraph()
            for u, v in self.subgraph.edges():
                if u < v:
                    dg.add_edge(u, v)
                else:
                    dg.add_edge(v, u)
            self.dependency_graph = dg
        return self.dependency_graph

    def _cal_degree_score(self):
        """
        Calculate a simple degree-based score: normalized degree centrality.
        """
        if self.dependency_graph is None:
            raise RuntimeError("Dependency graph not initialized.")
        centrality = nx.degree_centrality(self.dependency_graph)
        # Normalize to [0,1]
        max_c = max(centrality.values()) if centrality else 1
        self.degree_scores = {node: val / max_c for node, val in centrality.items()}
        return self.degree_scores

    def _cal_loss_score(self, node_to_score):
        """
        Calculate a loss score as the difference between the node's score
        and the average score of its neighbors.
        """
        if self.dependency_graph is None:
            raise RuntimeError("Dependency graph not initialized.")
        loss_scores = {}
        for node in self.dependency_graph.nodes():
            neighbors = list(self.dependency_graph.neighbors(node))
            if not neighbors:
                loss_scores[node] = 0.0
                continue
            avg_neighbor_score = sum(node_to_score.get(n, 0.0) for n in neighbors) / len(neighbors)
            loss_scores[node] = node_to_score.get(node, 0.0) - avg_neighbor_score
        self.loss_scores = loss_scores
        return self.loss_scores

    def _convert_DAG(self):
        """
        Convert the dependency graph to a DAG by topological sorting.
        If the graph contains cycles, we break them by removing edges
        that would create a cycle (simple heuristic).
        """
        if self.dependency_graph is None:
            raise RuntimeError("Dependency graph not initialized.")
        dg = self.dependency_graph.copy()
        try:
            order = list(nx.topological_sort(dg))
        except nx.NetworkXUnfeasible:
            # Graph has cycles; remove edges to break cycles
            cycles = list(nx.simple_cycles(dg))
            for cycle in cycles:
                # Remove one edge from each cycle
                u, v = cycle[0], cycle[1]
                if dg.has_edge(u, v):
                    dg.remove_edge(u, v)
            order = list(nx.topological_sort(dg))
        return order

    def _cal_degree_recon_score(self, degree_scores, recon_scores):
        """
        Combine degree and reconstruction (loss) scores.
        The combination is a weighted sum: 0.5 * degree + 0.5 * recon.
        """
        combined = {}
        for node in set(degree_scores) | set(recon_scores):
            d = degree_scores.get(node, 0.0)
            r = recon_scores.get(node, 0.0)
            combined[node] = 0.5 * d + 0.5 * r
        self.combined_scores = combined
        return combined