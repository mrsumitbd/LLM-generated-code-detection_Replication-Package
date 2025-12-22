def list_molalities_minerals(sr3):
    """
    Returns the lists of spatially distributed molalities and minerals.
    The input `sr3` can be one of the following:
        * A dictionary with keys 'molalities' and 'minerals'.
        * A pandas DataFrame with columns 'molality' and/or 'mineral'.
        * A NumPy array with at least two columns (molality, mineral).
        * A list of dictionaries or tuples/lists with molality and mineral values.
    The function attempts to extract the molality and mineral data in a
    flexible manner and returns two lists: (molalities, minerals).
    """
    molalities = []
    minerals = []

    # 1. Dictionary with explicit keys
    if isinstance(sr3, dict):
        if 'molalities' in sr3:
            molalities = list(sr3['molalities'])
        if 'minerals' in sr3:
            minerals = list(sr3['minerals'])
        # If keys are singular
        if not molalities and 'molality' in sr3:
            molalities = list(sr3['molality'])
        if not minerals and 'mineral' in sr3:
            minerals = list(sr3['mineral'])
        return molalities, minerals

    # 2. Pandas DataFrame
    try:
        import pandas as pd
        if isinstance(sr3, pd.DataFrame):
            if 'molality' in sr3.columns:
                molalities = sr3['molality'].tolist()
            elif 'molalities' in sr3.columns:
                molalities = sr3['molalities'].tolist()
            if 'mineral' in sr3.columns:
                minerals = sr3['mineral'].tolist()
            elif 'minerals' in sr3.columns:
                minerals = sr3['minerals'].tolist()
            return molalities, minerals
    except Exception:
        pass

    # 3. NumPy array
    try:
        import numpy as np
        if isinstance(sr3, np.ndarray):
            if sr3.ndim >= 2 and sr3.shape[1] >= 2:
                molalities = sr3[:, 0].tolist()
                minerals = sr3[:, 1].tolist()
                return molalities, minerals
    except Exception:
        pass

    # 4. List of dicts or tuples/lists
    if isinstance(sr3, (list, tuple)):
        for item in sr3:
            # dict case
            if isinstance(item, dict):
                if 'molality' in item:
                    molalities.append(item['molality'])
                elif 'molalities' in item:
                    molalities.append(item['molalities'])
                if 'mineral' in item:
                    minerals.append(item['mineral'])
                elif 'minerals' in item:
                    minerals.append(item['minerals'])
            # tuple/list case
            elif isinstance(item, (list, tuple)):
                if len(item) >= 2:
                    molalities.append(item[0])
                    minerals.append(item[1])
        return molalities, minerals

    # 5. Fallback: try to interpret as two separate iterables
    try:
        molalities = list(sr3[0])
        minerals = list(sr3[1])
        return molalities, minerals
    except Exception:
        pass

    # If nothing matched, return empty lists
    return molalities, minerals