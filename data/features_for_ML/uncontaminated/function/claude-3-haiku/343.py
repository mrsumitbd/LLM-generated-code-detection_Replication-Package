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
    rows = []
    for line in content.splitlines():
        if line.strip():
            parts = line.split("\t")
            geneset_name = parts[0]
            gene_symbols = parts[2:]
            for gene_symbol in gene_symbols:
                rows.append({geneset_key: geneset_name, genesymbol_key: gene_symbol})
    return pd.DataFrame(rows)