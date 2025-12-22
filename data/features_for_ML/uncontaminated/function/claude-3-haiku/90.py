import pandas as pd
from typing import Mapping, Optional, Any
from psycopg2.sql import Composed, SQL

def extract_df(
    cursor: CursorWrapper,
    query: sql.Composed | sql.SQL,
    dtype: Mapping[str, str],
    query_params: Optional[Mapping[str, Any]] = {},
    na_filter: bool = True,
    parse_dates: list[str] = [],
) -> pd.DataFrame:
    """
    Extracts a pandas DataFrame from a database query.

    Args:
        cursor (CursorWrapper): A database cursor object.
        query (sql.Composed | sql.SQL): The SQL query to execute.
        dtype (Mapping[str, str]): A dictionary mapping column names to data types.
        query_params (Optional[Mapping[str, Any]], optional): Parameters for the SQL query. Defaults to {}.
        na_filter (bool, optional): Whether to filter out missing values. Defaults to True.
        parse_dates (list[str], optional): List of column names to be parsed as dates. Defaults to [].

    Returns:
        pd.DataFrame: The resulting DataFrame.
    """
    cursor.execute(query, query_params)
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    df = df.astype(dtype)

    if na_filter:
        df = df.dropna()

    if parse_dates:
        df[parse_dates] = df[parse_dates].apply(pd.to_datetime)

    return df