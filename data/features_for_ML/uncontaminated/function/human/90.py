import pandas as pd
import io
from typing import Any, Collection, Iterable, Mapping, Optional, cast
from django.db.backends.utils import CursorWrapper
from psycopg import sql

def extract_df(
    cursor: CursorWrapper,
    query: sql.Composed | sql.SQL,
    dtype: Mapping[str, str],
    query_params: Optional[Mapping[str, Any]] = {},
    na_filter: bool = True,
    parse_dates: list[str] = [],
) -> pd.DataFrame:
    stmt = sql.SQL(
        "copy ({query}) to stdin with (format csv, header, delimiter ',')"
    ).format(
        query=query,
    )

    with cursor.copy(stmt, query_params) as copy:
        buffer = io.BytesIO()

        for data in copy:
            buffer.write(data)

        buffer.seek(0)

        return pd.read_csv(
            buffer, dtype=dtype, na_filter=na_filter, parse_dates=parse_dates
        )