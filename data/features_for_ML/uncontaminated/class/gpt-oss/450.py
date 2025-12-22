class Select:
    def __init__(self, *args):
        """
        Create a SELECT query builder.

        Usage:
            # Basic usage
            s = Select('users', 'id', 'name')
            s.where('age > 18').order_by('name').limit(10)

            # Raw query
            s = Select('SELECT * FROM users WHERE age > 18')
        """
        if not args:
            raise ValueError("At least one argument (table name or raw query) is required")

        # Raw query shortcut
        if len(args) == 1 and isinstance(args[0], str):
            self._raw = args[0]
            self._built = False
            return

        # Table name
        self._table = args[0]

        # Columns
        if len(args) > 1 and isinstance(args[1], (list, tuple)):
            self._columns = list(args[1])
        else:
            self._columns = list(args[1:]) if len(args) > 1 else ['*']

        # Query parts
        self._where = []
        self._order_by = []
        self._limit = None
        self._offset = None
        self._distinct = False
        self._group_by = []
        self._having = None

        self._built = True

    # ------------------------------------------------------------------
    # Query modifiers
    # ------------------------------------------------------------------
    def distinct(self):
        """Mark the query as DISTINCT."""
        self._distinct = True
        return self

    def where(self, condition):
        """
        Add a WHERE condition.

        Accepts:
            - A string: e.g. "age > 18"
            - A list/tuple of strings: e.g. ["age > 18", "status = 'active'"]
            - A dict: e.g. {"id": 5, "name": "John"} -> id = 5 AND name = 'John'
        """
        if isinstance(condition, dict):
            for k, v in condition.items():
                if isinstance(v, str):
                    v = f"'{v}'"
                self._where.append(f"{k} = {v}")
        elif isinstance(condition, (list, tuple)):
            self._where.extend(condition)
        else:
            self._where.append(condition)
        return self

    def order_by(self, column, asc=True):
        """Add an ORDER BY clause."""
        self._order_by.append((column, asc))
        return self

    def limit(self, n):
        """Add a LIMIT clause."""
        self._limit = n
        return self

    def offset(self, n):
        """Add an OFFSET clause."""
        self._offset = n
        return self

    def group_by(self, *columns):
        """Add a GROUP BY clause."""
        self._group_by.extend(columns)
        return self

    def having(self, condition):
        """Add a HAVING clause."""
        self._having = condition
        return self

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def to_sql(self):
        """Return the SQL string."""
        if not self._built:
            return self._raw

        parts = ["SELECT"]
        if self._distinct:
            parts.append("DISTINCT")
        parts.append(", ".join(self._columns))
        parts.append("FROM")
        parts.append(self._table)

        if self._where:
            parts.append("WHERE")
            parts.append(" AND ".join(self._where))

        if self._group_by:
            parts.append("GROUP BY")
            parts.append(", ".join(self._group_by))

        if self._having:
            parts.append("HAVING")
            parts.append(self._having)

        if self._order_by:
            parts.append("ORDER BY")
            parts.append(
                ", ".join(
                    f"{col} {'ASC' if asc else 'DESC'}" for col, asc in self._order_by
                )
            )

        if self._limit is not None:
            parts.append("LIMIT")
            parts.append(str(self._limit))

        if self._offset is not None:
            parts.append("OFFSET")
            parts.append(str(self._offset))

        return " ".join(parts)

    def __str__(self):
        return self.to_sql()

    def __repr__(self):
        return f"<Select: {self.to_sql()}>"