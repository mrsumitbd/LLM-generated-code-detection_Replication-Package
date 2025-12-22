import optuna
import pandas as pd

def load_trials_from_study(study: optuna.Study) -> tuple[pd.DataFrame, pd.DataFrame]:
    trials = study.trials
    trial_params = [trial.params for trial in trials]
    trial_values = [trial.value for trial in trials]
    
    df_params = pd.DataFrame(trial_params)
    df_values = pd.DataFrame(trial_values, columns=['value'])
    
    return df_params, df_values