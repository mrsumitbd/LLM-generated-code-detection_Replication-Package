def load_study(study_name: str) -> pd.DataFrame:
    import pandas as pd
    import os
    
    # Try common file extensions and locations
    possible_paths = [
        study_name,
        f"{study_name}.csv",
        f"{study_name}.xlsx",
        f"{study_name}.json",
        f"{study_name}.parquet",
        os.path.join("data", study_name),
        os.path.join("data", f"{study_name}.csv"),
        os.path.join("data", f"{study_name}.xlsx"),
        os.path.join("data", f"{study_name}.json"),
        os.path.join("data", f"{study_name}.parquet"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            if path.endswith('.csv'):
                return pd.read_csv(path)
            elif path.endswith('.xlsx'):
                return pd.read_excel(path)
            elif path.endswith('.json'):
                return pd.read_json(path)
            elif path.endswith('.parquet'):
                return pd.read_parquet(path)
            else:
                # Try to infer format
                try:
                    return pd.read_csv(path)
                except:
                    try:
                        return pd.read_json(path)
                    except:
                        return pd.read_parquet(path)
    
    raise FileNotFoundError(f"Study '{study_name}' not found in any expected location")