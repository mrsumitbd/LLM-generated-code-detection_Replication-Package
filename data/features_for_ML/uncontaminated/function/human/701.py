import optuna
import pandas as pd

def load_trials_from_study(study: optuna.Study) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Get all trials
    trials_df = study.trials_dataframe()

    # Get Pareto optimal trials
    pareto_trials = study.best_trials
    pareto_trial_numbers = [trial.number for trial in pareto_trials]
    pareto_trials_df = trials_df[trials_df['number'].isin(pareto_trial_numbers)]

    return trials_df, pareto_trials_df