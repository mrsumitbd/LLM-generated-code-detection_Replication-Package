import networkx as nx

class DEPIMPACT:

    def __init__(self, graph, poi, node_to_score, used_method, score_method):
        self.graph = graph
        self.poi = poi
        self.node_to_score = node_to_score
        self.used_method = used_method
        self.score_method = score_method

    def run(self):
        subgraph_nodes = self.n_hop_subgraph_nodes()
        dependency_graph = self.gen_dependency_graph(subgraph_nodes)
        return dependency_graph

    def n_hop_subgraph_nodes(self):
        # Implementation of n_hop_subgraph_nodes method
        pass

    def gen_dependency_graph(self, subgraph_nodes):
        # Implementation of gen_dependency_graph method
        pass

    def _cal_degree_score(self):
        # Implementation of _cal_degree_score method
        pass

    def _cal_loss_score(self, node_to_score):
        # Implementation of _cal_loss_score method
        pass

    def _convert_DAG(self):
        # Implementation of _convert_DAG method
        pass

    def _cal_degree_recon_score(self, degree_scores, recon_scores):
        # Implementation of _cal_degree_recon_score method
        pass