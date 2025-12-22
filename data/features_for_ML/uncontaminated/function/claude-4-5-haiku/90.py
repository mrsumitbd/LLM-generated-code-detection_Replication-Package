def extract_df(
    cursor: CursorWrapper,
    query: sql.Composed | sql.SQL,
    dtype: Mapping[str, str],
    query_params: Optional[Mapping[str, Any]] = {},
    na_filter: bool = True,
    parse_dates: list[str] = [],
) -> pd.DataFrame:
    cursor.execute(query, query_params)
    
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows, columns=columns)
    
    if len(df) == 0:
        for col, dtype_str in dtype.items():
            if col in df.columns:
                df[col] = df[col].astype(dtype_str)
        return df
    
    for col, dtype_str in dtype.items():
        if col in df.columns:
            df[col] = df[col].astype(dtype_str)
    
    for col in parse_dates:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    
    return df