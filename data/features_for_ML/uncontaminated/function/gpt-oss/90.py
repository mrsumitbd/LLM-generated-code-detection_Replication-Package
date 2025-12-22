import pandas as pd
from typing import Mapping, Optional, Any, Iterable, List

def extract_df(
    cursor: "CursorWrapper",
    query: "sql.Composed | sql.SQL",
    dtype: Mapping[str, str],
    query_params: Optional[Mapping[str, Any]] = None,
    na_filter: bool = True,
    parse_dates: List[str] = None,
) -> pd.DataFrame:
    """
    Execute a SQL query and return the result as a pandas DataFrame.

    Parameters
    ----------
    cursor : CursorWrapper
        Database cursor used to execute the query.
    query : sql.Composed | sql.SQL
        The SQL query to execute.  It may be a string or an object that
        implements ``as_string``.
    dtype : Mapping[str, str]
        Mapping of column names to desired pandas dtype strings.
    query_params : Mapping[str, Any], optional
        Parameters to pass to the query.
    na_filter : bool, default True
        If True, drop rows where all values are NA.
    parse_dates : list[str], optional
        List of column names to parse as datetime.

    Returns
    -------
    pd.DataFrame
        The query result as a DataFrame.
    """
    if query_params is None:
        query_params = {}

    # Convert query to string if necessary
    if hasattr(query, "as_string"):
        sql_str = query.as_string(cursor)
    else:
        sql_str = str(query)

    # Execute query
    cursor.execute(sql_str, query_params)

    # Fetch column names
    colnames = [desc[0] for desc in cursor.description]

    # Fetch all rows
    rows = cursor.fetchall()

    # Build DataFrame
    df = pd.DataFrame(rows, columns=colnames)

    # Apply dtype mapping
    for col, col_dtype in dtype.items():
        if col in df.columns:
            try:
                df[col] = df[col].astype(col_dtype)
            except Exception:
                # If conversion fails, leave as is
                pass

    # Parse dates
    if parse_dates:
        for col in parse_dates:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

    # Apply na_filter
    if na_filter:
        df.dropna(how="all", inplace=True)

    return df