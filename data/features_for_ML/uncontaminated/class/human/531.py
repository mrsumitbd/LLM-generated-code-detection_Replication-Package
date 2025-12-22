import networkx as nx
from pidsmaker.utils.utils import get_node_to_path_and_type, log, log_tqdm

class DEPIMPACT:
    def __init__(self, graph, poi, node_to_score, used_method, score_method):
        self.graph = graph
        self.poi = poi
        self.used_method = used_method
        self.score_method = score_method

        log_with_pid(
            f"Start trace with args used method: {used_method} and score method: {score_method}"
        )

        if self.score_method == "degree":
            self.node_scores = self._cal_degree_score()
        elif self.score_method == "recon_loss":
            self.node_scores = self._cal_loss_score(node_to_score)
        elif self.score_method == "degree_recon":
            degree_scores = self._cal_degree_score()
            recon_scores = self._cal_loss_score(node_to_score)
            self.node_scores = self._cal_degree_recon_score(degree_scores, recon_scores)

    def run(self):
        if self.used_method == "component" or self.used_method == "shortest_path":
            subgraph_nodes = self.gen_dependency_graph()
        elif (
            self.used_method == "1-hop"
            or self.used_method == "2-hop"
            or self.used_method == "3-hop"
        ):
            subgraph_nodes = self.n_hop_subgraph_nodes()

        return subgraph_nodes

    def n_hop_subgraph_nodes(self):
        graph = self.graph
        poi = self.poi
        n = int(self.used_method.split("-")[0])

        subgraph_nodes = get_n_hop_neighbors(graph, poi, n)

        return subgraph_nodes

    def gen_dependency_graph(self):
        poi_in_graph = self.poi

        if self.used_method == "shortest_path":
            self.dag, self.backward_poi = self._convert_DAG()
            backward_poi = self.backward_poi
            forward_poi = str(self.poi) + "-" + str(0)
        elif self.used_method == "component":
            self.dag, self.backward_poi = self._convert_DAG()
            backward_poi = self.backward_poi
            forward_poi = str(self.poi) + "-" + str(0)

        subgraph_nodes = set()

        in_deg = self.dag.in_degree(backward_poi)
        if isinstance(in_deg, int) and in_deg > 0:
            if self.used_method == "shortest_path":
                entry2path = dag_backward_tracing_shortest_path(backward_poi, self.dag)
            elif self.used_method == "component":
                entry2path = dag_backward_tracing_component(backward_poi, self.dag)
            entry2nodes = {}
            for entry, paths in entry2path.items():
                entry_in_graph = entry.split("-")[0]
                if entry_in_graph not in entry2nodes:
                    entry2nodes[entry_in_graph] = set()

                nodes_in_dag = set()
                for path in paths:
                    nodes_in_dag |= set(path)

                for node_in_dag in list(nodes_in_dag):
                    node_in_graph = node_in_dag.split("-")[0]
                    entry2nodes[entry_in_graph].add(node_in_graph)

            entry2score = {}
            for entry, nodes in entry2nodes.items():
                nodes.discard(poi_in_graph)
                node_scores = []
                for node in nodes:
                    node_scores.append(self.node_scores[node])

                if len(node_scores) == 0:
                    entry2score[entry] = 0
                else:
                    entry2score[entry] = sum(node_scores) / len(node_scores)

            entry_scores = []
            for e, score in entry2score.items():
                entry_scores.append((e, score))
            max_entry_score = max(entry_scores, key=lambda x: x[1])[1]
            highest_entries = [item[0] for item in entry_scores if item[1] == max_entry_score]

            for he in highest_entries:
                subgraph_nodes |= entry2nodes[he]
        else:
            print(f"POI {backward_poi} is an entry node, skip backward tracing.")

        out_deg = self.dag.out_degree(forward_poi)
        if isinstance(out_deg, int) and out_deg > 0:
            if self.used_method == "shortest_path":
                exit2path = dag_forward_tracing_shortest_path(forward_poi, self.dag)
            elif self.used_method == "component":
                exit2path = dag_forward_tracing_component(forward_poi, self.dag)
            exit2nodes = {}
            for exit, paths in exit2path.items():
                exit_in_graph = exit.split("-")[0]
                if exit_in_graph not in exit2nodes:
                    exit2nodes[exit_in_graph] = set()

                nodes_in_dag = set()
                for path in paths:
                    nodes_in_dag |= set(path)

                for node_in_dag in list(nodes_in_dag):
                    node_in_graph = node_in_dag.split("-")[0]
                    exit2nodes[exit_in_graph].add(node_in_graph)

            exit2score = {}
            for exit, nodes in exit2nodes.items():
                nodes.discard(poi_in_graph)
                node_scores = []
                for node in nodes:
                    node_scores.append(self.node_scores[node])

                if len(node_scores) == 0:
                    exit2score[exit] = 0
                else:
                    exit2score[exit] = sum(node_scores) / len(node_scores)

            exit_scores = []
            for e, score in exit2score.items():
                exit_scores.append((e, score))
            max_exit_score = max(exit_scores, key=lambda x: x[1])[1]
            highest_entries = [item[0] for item in exit_scores if item[1] == max_exit_score]

            for he in highest_entries:
                subgraph_nodes |= exit2nodes[he]
        else:
            print(f"POI {forward_poi} is an exit node, skip forward tracing.")

        subgraph_nodes.add(poi_in_graph)

        return subgraph_nodes

    def _cal_degree_score(self):
        out_to_in = {}
        in_degrees = dict(self.graph.in_degree())
        out_degrees = dict(self.graph.out_degree())
        for node in log_tqdm(self.graph.nodes(), desc="calculating degree score"):
            if int(in_degrees[node]) == 0:
                out_to_in[node] = 0
            else:
                out_to_in[node] = int(out_degrees[node]) / int(in_degrees[node])
        return out_to_in

    def _cal_loss_score(self, node_to_score):
        node_scores = {}
        for node in log_tqdm(self.graph.nodes(), desc="calculating degree score"):
            if str(node) in node_scores:
                node_scores[node] = int(node_to_score[str(node)])
            else:
                node_scores[node] = 0
        return node_scores

    def _convert_DAG(self):
        graph = self.graph
        edges = []
        node_version = {}
        for u, v, k, data in graph.edges(keys=True, data=True):
            edges.append((u, v, int(data["time"])))
            if u not in node_version:
                node_version[u] = 0
            if v not in node_version:
                node_version[v] = 0

        sorted_edges = sorted(edges, key=lambda x: x[2])

        new_nodes = set()
        new_edges = []
        visited = set()
        for u, v, t in sorted_edges:
            # if u == v:
            #     continue

            src = str(u) + "-" + str(node_version[u])
            visited.add(u)
            new_nodes.add(src)

            if v not in visited:
                dst = str(v) + "-" + str(node_version[v])
                visited.add(v)
                new_nodes.add(dst)
                new_edges.append((src, dst, {"time": int(t)}))
            else:
                dst_current = str(v) + "-" + str(node_version[v])
                dst_new = str(v) + "-" + str(node_version[v] + 1)
                node_version[v] += 1
                new_nodes.add(dst_new)
                new_edges.append((src, dst_new, {"time": int(t)}))
                new_edges.append((dst_current, dst_new, {"time": int(t)}))

        DAG = nx.DiGraph()
        DAG.add_nodes_from(list(new_nodes))
        DAG.add_edges_from(new_edges)

        old_poi = self.poi
        new_poi = str(old_poi) + "-" + str(node_version[old_poi])

        return DAG, new_poi

    def _cal_degree_recon_score(self, degree_scores, recon_scores):
        nid_list = []
        degree_score_list = []
        recon_score_list = []
        for node, score in degree_scores.items():
            nid_list.append(node)
            degree_score_list.append(score)
            recon_score_list.append(recon_scores[node])

        normalized_degree_score_list = min_max_normalize(degree_score_list)
        normalized_recon_score_list = min_max_normalize(recon_score_list)

        node_scores = {}
        for i in range(len(nid_list)):
            node_scores[nid_list[i]] = (
                normalized_degree_score_list[i] + normalized_recon_score_list[i]
            )

        return node_scores