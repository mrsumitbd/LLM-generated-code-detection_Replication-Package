def prep(df):
        df = df.copy()
        df[merge_cols] = df[merge_cols].astype(str)
        df = df.groupby(merge_cols, dropna=False)[value_col].median().reset_index()
        return df