from typing import Any, List

from sqlalchemy.orm.attributes import QueryableAttribute

from .errors import TranspilingError  # Adjust import path as needed


def expressions(self) -> List[QueryableAttribute[Any]]:
    """
    Creates DISTINCT ON expressions from the fields specified in the query graph.

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
    # Retrieve the list of fields that should be used for DISTINCT ON.
    distinct_fields = self._distinct_on_fields()

    # If no DISTINCT ON fields are specified, nothing to do.
    if not distinct_fields:
        return []

    # Grab the ORDER BY nodes from the query graph.
    order_by_nodes = getattr(self.query_graph, "order_by_nodes", None)

    # PostgreSQL requires an ORDER BY clause when DISTINCT ON is used.
    if not order_by_nodes:
        raise TranspilingError(
            "DISTINCT ON requires an ORDER BY clause, but none was found."
        )

    # Extract the field names from the ORDER BY nodes.
    # We assume each node has a `field` attribute that holds the field name.
    order_by_fields = [getattr(node, "field", None) for node in order_by_nodes]

    # Validate that the DISTINCT ON fields match the leftmost ORDER BY fields.
    if order_by_fields[: len(distinct_fields)] != distinct_fields:
        raise TranspilingError(
            "DISTINCT ON fields must match the leftmost ORDER BY fields."
        )

    # Convert the field names to QueryableAttribute objects.
    # We assume the query graph provides a helper to fetch the attribute
    # given a field name. If the field is already an attribute, we keep it.
    attributes: List[QueryableAttribute[Any]] = []
    for field in distinct_fields:
        if isinstance(field, QueryableAttribute):
            attributes.append(field)
        else:
            # Attempt to fetch the attribute from the query graph.
            try:
                attr = getattr(self.query_graph, field)
            except AttributeError as exc:
                raise TranspilingError(
                    f"Field '{field}' specified for DISTINCT ON does not exist."
                ) from exc
            attributes.append(attr)

    return attributes