import pandas as pd

def load_study(study_name: str) -> pd.DataFrame:
    # load the study
    study_data = pd.read_csv(f"{study_name}.csv")
    return study_data