import pandas as pd

def gmt_to_dataframe(content: str, geneset_key: str = "geneset", genesymbol_key: str = "genesymbol") -> pd.DataFrame:
    """
    Convert GMT content to a pandas DataFrame with one gene per row.

    Parameters
    ----------
        content : str
            Content of the GMT file.
        geneset_key : str
            Column name for the gene set name.
        genesymbol_key : str
            Column name for the gene symbol.

    Returns
    -------
        pd.DataFrame: DataFrame with columns [geneset_key, genesymbol_key], where each row corresponds to a gene in a gene set.
    """
    records = parse_gmt(content, geneset_key, "genesymbols")
    rows = [{geneset_key: rec[geneset_key], genesymbol_key: gene} for rec in records for gene in rec["genesymbols"]]
    return pd.DataFrame(rows)