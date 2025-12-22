from sqlalchemy import (
    CTE,
    AliasedReturnsRows,
    BooleanClauseList,
    Label,
    Lateral,
    Select,
    Subquery,
    UnaryExpression,
    func,
    inspect,
    null,
    select,
)
from sqlalchemy.orm import (
    QueryableAttribute,
    RelationshipDirection,
    RelationshipProperty,
    aliased,
    class_mapper,
    raiseload,
)
from .exceptions import TranspilingError
from typing import TYPE_CHECKING, Any, Generic, Optional, Union, cast

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
        for i, distinct_field in enumerate(self._distinct_on_fields):
            if i > len(self.query_graph.order_by_nodes) - 1:
                break
            if self.query_graph.order_by_nodes[i].value.model_field is distinct_field.model_field:
                continue
            msg = "Distinct on fields must match the leftmost order by fields"
            raise TranspilingError(msg)
        return [
            field.model_field.adapt_to_entity(inspect(self.query_graph.scope.root_alias))
            for field in self._distinct_on_fields
        ]