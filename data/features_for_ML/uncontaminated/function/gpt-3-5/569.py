def expressions(self) -> list[QueryableAttribute[Any]]:
    distinct_on_fields = self._distinct_on_fields
    order_by_nodes = self.query_graph.order_by_nodes

    if not order_by_nodes:
        raise TranspilingError("ORDER BY is required when DISTINCT ON is used")

    distinct_on_expressions = []
    for field in distinct_on_fields:
        found = False
        for node in order_by_nodes:
            if node.expression == field:
                distinct_on_expressions.append(node.expression)
                found = True
                break
        if not found:
            raise TranspilingError("DISTINCT ON fields do not correspond to the leftmost ORDER BY fields")

    return distinct_on_expressions