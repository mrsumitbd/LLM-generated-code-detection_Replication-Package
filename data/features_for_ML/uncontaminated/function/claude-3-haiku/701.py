import pandas as pd

def load_trials_from_study(study: optuna.Study) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Get all trials
    trials = study.get_trials()

    # Create dataframes for completed and pruned trials
    completed_trials = pd.DataFrame([t.to_dict() for t in trials if t.state == optuna.trial.TrialState.COMPLETE])
    pruned_trials = pd.DataFrame([t.to_dict() for t in trials if t.state == optuna.trial.TrialState.PRUNED])

    return completed_trials, pruned_trials