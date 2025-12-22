def expressions(self) -> list[UnaryExpression[Any]]:
    """Generates a list of SQLAlchemy UnaryExpression objects for the ORDER BY clause.

    This method iterates through the `columns` and uses the `_order_by` method
    to convert each column and its ordering specification into the appropriate
    SQLAlchemy expression (e.g., `column.asc()`, `column.desc().nulls_first()`).

    Returns:
        A list of SQLAlchemy UnaryExpression objects ready to be applied to a query.
    """
    return [self._order_by(column) for column in self.columns]