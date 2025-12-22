def avg_out_degree(self):
    """
    Average out-degree (only for directed graphs).
    """
    if self.number_of_nodes() == 0:
        return 0
    
    total_out_degree = sum(self.out_degree(node) for node in self.nodes())
    return total_out_degree / self.number_of_nodes()