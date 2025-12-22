def expressions(self) -> list[UnaryExpression[Any]]:
    """Generates a list of SQLAlchemy UnaryExpression objects for the ORDER BY clause.

    This method iterates through the `columns` and uses the `_order_by` method
    to convert each column and its ordering specification into the appropriate
    SQLAlchemy expression (e.g., `column.asc()`, `column.desc().nulls_first()`).

    Returns:
        A list of SQLAlchemy UnaryExpression objects ready to be applied to a query.
    """
    expressions = []
    for column, order_by in self.columns:
        expressions.append(self._order_by(column, order_by))
    return expressions

def _order_by(self, column, order_by):
    if order_by == 'asc':
        return column.asc()
    elif order_by == 'desc':
        return column.desc()
    elif order_by == 'desc_nulls_first':
        return column.desc().nulls_first()
    elif order_by == 'desc_nulls_last':
        return column.desc().nulls_last()
    elif order_by == 'asc_nulls_first':
        return column.asc().nulls_first()
    elif order_by == 'asc_nulls_last':
        return column.asc().nulls_last()
    else:
        raise ValueError(f"Invalid order_by value: {order_by}")