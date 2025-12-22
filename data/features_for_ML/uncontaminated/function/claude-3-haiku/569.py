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
    distinct_on_fields = self._distinct_on_fields()
    order_by_nodes = self.query_graph.order_by_nodes

    if not order_by_nodes and distinct_on_fields:
        raise TranspilingError(
            "DISTINCT ON is used, but ORDER BY is not specified, which is required by the database."
        )

    distinct_on_expressions = []
    for field in distinct_on_fields:
        matching_order_by_nodes = [
            node for node in order_by_nodes if node.get_label() == field
        ]
        if not matching_order_by_nodes:
            raise TranspilingError(
                f"DISTINCT ON field '{field}' does not correspond to any ORDER BY field."
            )
        distinct_on_expressions.append(matching_order_by_nodes[0].get_expression())

    return distinct_on_expressions