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
    import pandas as pd
    
    data = []
    
    for line in content.strip().split('\n'):
        if not line.strip():
            continue
        
        parts = line.strip().split('\t')
        
        if len(parts) < 3:
            continue
        
        geneset_name = parts[0]
        genes = parts[2:]
        
        for gene in genes:
            if gene.strip():
                data.append({geneset_key: geneset_name, genesymbol_key: gene.strip()})
    
    return pd.DataFrame(data)