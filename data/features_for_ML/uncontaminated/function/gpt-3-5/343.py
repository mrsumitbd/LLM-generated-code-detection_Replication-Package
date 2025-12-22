import pandas as pd
from io import StringIO

def gmt_to_dataframe(content: str, geneset_key: str = "geneset", genesymbol_key: str = "genesymbol") -> pd.DataFrame:
    data = []
    for line in content.strip().split('\n'):
        parts = line.split('\t')
        geneset = parts[0]
        for gene in parts[2:]:
            data.append([geneset, gene])
    return pd.DataFrame(data, columns=[geneset_key, genesymbol_key])