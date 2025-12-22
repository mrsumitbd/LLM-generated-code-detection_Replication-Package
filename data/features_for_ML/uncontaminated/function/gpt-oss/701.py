import pandas as pd
import optuna

def load_trials_from_study(study: optuna.Study) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load all trials from an Optuna study into two pandas DataFrames.

    Parameters
    ----------
    study : optuna.Study
        The Optuna study from which to extract trial information.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        A tuple containing:
        1. A DataFrame with trial metadata (trial number, timestamps, value, state, attrs).
        2. A DataFrame with trial parameters, one column per parameter and a column for the trial number.
    """
    trials = study.trials

    # If there are no trials, return empty DataFrames
    if not trials:
        return pd.DataFrame(), pd.DataFrame()

    # Build trial metadata DataFrame
    trial_meta = []
    for trial in trials:
        trial_meta.append({
            "trial_number": trial.number,
            "datetime_start": trial.datetime_start,
            "datetime_complete": trial.datetime_complete,
            "value": trial.value,
            "state": trial.state,
            "user_attrs": trial.user_attrs,
            "system_attrs": trial.system_attrs,
        })
    df_trials = pd.DataFrame(trial_meta)

    # Build parameters DataFrame
    params_list = []
    for trial in trials:
        params = trial.params.copy()
        params["trial_number"] = trial.number
        params_list.append(params)
    df_params = pd.DataFrame(params_list)

    # Ensure consistent ordering by trial number
    df_trials = df_trials.sort_values("trial_number").reset_index(drop=True)
    df_params = df_params.sort_values("trial_number").reset_index(drop=True)

    return df_trials, df_params