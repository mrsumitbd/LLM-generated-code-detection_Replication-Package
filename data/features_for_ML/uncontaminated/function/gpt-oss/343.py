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
    for line in content.strip().splitlines():
        if not line or line.startswith("#"):
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue  # skip malformed lines
        geneset = parts[0].strip()
        # parts[1] is description, ignored
        for gene in parts[2:]:
            gene = gene.strip()
            if gene:
                rows.append({geneset_key: geneset, genesymbol_key: gene})
    return pd.DataFrame(rows, columns=[geneset_key, genesymbol_key])