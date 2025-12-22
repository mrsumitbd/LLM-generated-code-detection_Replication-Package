def expressions(self) -> list[UnaryExpression[Any]]:
    expressions = []
    for column, order_spec in self.columns.items():
        expression = self._order_by(column, order_spec)
        expressions.append(expression)
    return expressions