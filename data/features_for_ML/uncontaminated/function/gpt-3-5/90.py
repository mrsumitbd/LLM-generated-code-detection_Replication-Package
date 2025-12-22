import pandas as pd
from psycopg2.sql import Composed, SQL
from psycopg2.extensions import Cursor
from typing import Mapping, Any, Optional

def extract_df(
    cursor: Cursor,
    query: Composed | SQL,
    dtype: Mapping[str, str],
    query_params: Optional[Mapping[str, Any]] = {},
    na_filter: bool = True,
    parse_dates: list[str] = [],
) -> pd.DataFrame:
    
    cursor.execute(query, query_params)
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    
    df = pd.DataFrame(data, columns=columns)
    
    for col, col_type in dtype.items():
        df[col] = df[col].astype(col_type)
    
    if na_filter:
        df.replace('', pd.NA, inplace=True)
    
    for col in parse_dates:
        df[col] = pd.to_datetime(df[col])
    
    return df