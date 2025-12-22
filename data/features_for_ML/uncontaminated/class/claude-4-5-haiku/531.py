class DEPIMPACT:

    def __init__(self, graph, poi, node_to_score, used_method, score_method):
        self.graph = graph
        self.poi = poi
        self.node_to_score = node_to_score
        self.used_method = used_method
        self.score_method = score_method
        self.n_hop_nodes = set()
        self.dependency_graph = None
        self.degree_scores = {}
        self.loss_scores = {}
        self.recon_scores = {}
        self.final_scores = {}

    def run(self):
        self.n_hop_subgraph_nodes()
        self.gen_dependency_graph()
        self._cal_degree_score()
        self._cal_loss_score(self.node_to_score)
        self._convert_DAG()
        self._cal_degree_recon_score(self.degree_scores, self.loss_scores)
        return self.final_scores

    def n_hop_subgraph_nodes(self):
        visited = set()
        queue = [self.poi]
        visited.add(self.poi)
        
        while queue:
            node = queue.pop(0)
            self.n_hop_nodes.add(node)
            
            if node in self.graph:
                for neighbor in self.graph[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
        
        return self.n_hop_nodes

    def gen_dependency_graph(self):
        self.dependency_graph = {}
        
        for node in self.n_hop_nodes:
            self.dependency_graph[node] = []
            
            if node in self.graph:
                for neighbor in self.graph[node]:
                    if neighbor in self.n_hop_nodes:
                        self.dependency_graph[node].append(neighbor)
        
        return self.dependency_graph

    def _cal_degree_score(self):
        for node in self.n_hop_nodes:
            in_degree = 0
            out_degree = 0
            
            for other_node in self.n_hop_nodes:
                if other_node in self.dependency_graph:
                    if node in self.dependency_graph[other_node]:
                        in_degree += 1
            
            if node in self.dependency_graph:
                out_degree = len(self.dependency_graph[node])
            
            self.degree_scores[node] = in_degree + out_degree

    def _cal_loss_score(self, node_to_score):
        for node in self.n_hop_nodes:
            if node in node_to_score:
                self.loss_scores[node] = node_to_score[node]
            else:
                self.loss_scores[node] = 0

    def _convert_DAG(self):
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            
            if node in self.dependency_graph:
                for neighbor in self.dependency_graph[node]:
                    if neighbor not in visited:
                        if has_cycle(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        return True
            
            rec_stack.remove(node)
            return False
        
        for node in self.n_hop_nodes:
            if node not in visited:
                has_cycle(node)

    def _cal_degree_recon_score(self, degree_scores, recon_scores):
        for node in self.n_hop_nodes:
            degree_score = degree_scores.get(node, 0)
            recon_score = recon_scores.get(node, 0)
            
            if self.score_method == "combined":
                self.final_scores[node] = 0.5 * degree_score + 0.5 * recon_score
            elif self.score_method == "degree":
                self.final_scores[node] = degree_score
            elif self.score_method == "loss":
                self.final_scores[node] = recon_score
            else:
                self.final_scores[node] = degree_score + recon_score
        
        return self.final_scores