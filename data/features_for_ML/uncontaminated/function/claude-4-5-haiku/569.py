def expressions(self) -> list[QueryableAttribute[Any]]:
    """Creates DISTINCT ON expressions from the fields specified in the query graph.

    This method retrieves the fields intended for `DISTINCT ON` using
    `_distinct_on_fields`. It then validates these fields against the
    `order_by_nodes` from the `query_graph`. For `DISTINCT ON` to be valid
    (especially in PostgreSQL), the expressions in `DISTINCT ON` must match
    the leftmost expressions in the `ORDER BY` clause.

    Returns:
        A list of SQLAlchemy `QueryableAttribute` objects that can be used
        in a `SELECT.distinct(*attributes)` call.

    Raises:
        TranspilingError: If the `DISTINCT ON` fields do not correspond to the
            leftmost `ORDER BY` fields, or if `ORDER BY` is not specified when
            `DISTINCT ON` is used (and the database requires it).
    """
    from sqlalchemy.orm import QueryableAttribute
    from sqlalchemy.exc import InvalidRequestError
    
    distinct_on_fields = self._distinct_on_fields
    
    if not distinct_on_fields:
        return []
    
    order_by_nodes = self.query_graph.order_by_nodes
    
    if not order_by_nodes:
        raise TranspilingError(
            "DISTINCT ON requires ORDER BY clause to be specified"
        )
    
    expressions_list: list[QueryableAttribute[Any]] = []
    
    for field in distinct_on_fields:
        attr = self.query_graph.get_attribute(field)
        expressions_list.append(attr)
    
    if len(expressions_list) > len(order_by_nodes):
        raise TranspilingError(
            "DISTINCT ON fields must not exceed ORDER BY fields"
        )
    
    for i, expr in enumerate(expressions_list):
        order_by_expr = order_by_nodes[i]
        if not self._expressions_match(expr, order_by_expr):
            raise TranspilingError(
                f"DISTINCT ON field at position {i} does not match "
                f"the corresponding ORDER BY field"
            )
    
    return expressions_list