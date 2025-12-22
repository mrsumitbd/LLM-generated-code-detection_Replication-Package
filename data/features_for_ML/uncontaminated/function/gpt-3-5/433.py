def avg_out_degree(self):
    if not self.is_directed():
        raise ValueError("Average out-degree is only defined for directed graphs.")
    
    total_out_degree = sum(self.out_degree(node) for node in self.nodes())
    return total_out_degree / self.number_of_nodes() if self.number_of_nodes() > 0 else 0