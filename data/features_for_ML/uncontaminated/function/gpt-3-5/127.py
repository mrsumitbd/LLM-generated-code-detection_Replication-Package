def prep(df):
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df