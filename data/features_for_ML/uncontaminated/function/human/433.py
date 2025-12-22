def avg_out_degree(self):
        """
        Average out-degree (only for directed graphs).
        """
        if not self.g.is_directed():
            raise ValueError("Graph is not directed")
        n = self.g.number_of_nodes()
        return sum(dict(self.g.out_degree()).values()) / n if n > 0 else 0