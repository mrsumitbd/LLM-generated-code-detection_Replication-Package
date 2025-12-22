import re

def process_statement(statement, column_names=[]):
    """
    Very small SQL statement processor.

    Supports:
        * INSERT INTO <table> [(col1, col2, ...)] VALUES (val1, val2, ...)
          If the column list is omitted, `column_names` must be supplied.
          Returns a dict mapping column names to values (values are returned
          as strings with surrounding quotes removed).

        * SELECT col1, col2, ... FROM <table>
          Returns a list of column names.

    Raises:
        ValueError: if the statement cannot be parsed or if the number of
                    columns does not match the number of values.
        NotImplementedError: for unsupported statement types.
    """
    stmt = statement.strip()

    # INSERT statement
    if stmt.upper().startswith("INSERT"):
        # Regex to capture table name, optional column list, and values list
        insert_re = re.compile(
            r"INSERT\s+INTO\s+(\w+)"          # table name
            r"\s*(?:\(([^)]+)\))?"           # optional column list
            r"\s+VALUES\s*\(([^)]+)\)",      # values list
            re.IGNORECASE
        )
        m = insert_re.match(stmt)
        if not m:
            raise ValueError(f"Unsupported INSERT statement: {statement}")

        table_name, cols_str, vals_str = m.groups()

        # Parse columns
        if cols_str:
            cols = [c.strip() for c in cols_str.split(",")]
        else:
            if not column_names:
                raise ValueError("Column names must be provided when omitted in INSERT")
            cols = column_names

        # Parse values
        vals = [v.strip().strip("'\"") for v in vals_str.split(",")]

        if len(cols) != len(vals):
            raise ValueError(
                f"Column count ({len(cols)}) does not match value count ({len(vals)})"
            )

        return dict(zip(cols, vals))

    # SELECT statement
    if stmt.upper().startswith("SELECT"):
        select_re = re.compile(
            r"SELECT\s+(.+?)\s+FROM\s+(\w+)", re.IGNORECASE
        )
        m = select_re.match(stmt)
        if not m:
            raise ValueError(f"Unsupported SELECT statement: {statement}")

        cols_str = m.group(1)
        cols = [c.strip() for c in cols_str.split(",")]
        return cols

    raise NotImplementedError(f"Unsupported statement type: {statement}")