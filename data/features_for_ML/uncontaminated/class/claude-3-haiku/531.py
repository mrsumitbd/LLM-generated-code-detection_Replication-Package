import networkx as nx
import numpy as np
from collections import defaultdict

class DEPIMPACT:

    def __init__(self, graph, poi, node_to_score, used_method, score_method):
        self.graph = graph
        self.poi = poi
        self.node_to_score = node_to_score
        self.used_method = used_method
        self.score_method = score_method
        self.n_hop_subgraph = None
        self.dependency_graph = None
        self.degree_scores = None
        self.recon_scores = None

    def run(self):
        self.n_hop_subgraph_nodes()
        self.gen_dependency_graph()
        self._cal_degree_score()
        self._cal_loss_score(self.node_to_score)
        self._convert_DAG()
        self._cal_degree_recon_score(self.degree_scores, self.recon_scores)

    def n_hop_subgraph_nodes(self):
        self.n_hop_subgraph = nx.ego_graph(self.graph, self.poi, radius=2)

    def gen_dependency_graph(self):
        self.dependency_graph = nx.DiGraph()
        for node in self.n_hop_subgraph.nodes():
            self.dependency_graph.add_node(node)
        for u, v in self.n_hop_subgraph.edges():
            self.dependency_graph.add_edge(u, v)

    def _cal_degree_score(self):
        self.degree_scores = {node: self.dependency_graph.out_degree(node) for node in self.dependency_graph.nodes()}

    def _cal_loss_score(self, node_to_score):
        self.recon_scores = {node: node_to_score[node] for node in self.dependency_graph.nodes()}

    def _convert_DAG(self):
        self.dependency_graph = nx.DiGraph([(u, v) for u, v in self.dependency_graph.edges() if u < v])

    def _cal_degree_recon_score(self, degree_scores, recon_scores):
        self.score = {node: degree_scores[node] * recon_scores[node] for node in self.dependency_graph.nodes()}