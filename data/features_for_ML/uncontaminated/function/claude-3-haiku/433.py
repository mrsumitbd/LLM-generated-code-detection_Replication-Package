def avg_out_degree(self):
    """
    Average out-degree (only for directed graphs).
    """
    total_out_degree = 0
    for node in self.nodes():
        total_out_degree += self.out_degree(node)
    return total_out_degree / self.number_of_nodes()