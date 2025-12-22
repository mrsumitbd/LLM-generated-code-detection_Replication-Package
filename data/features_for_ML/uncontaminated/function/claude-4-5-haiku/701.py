def load_trials_from_study(study: optuna.Study) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Get all trials
    trials = study.trials
    
    # Separate completed and incomplete trials
    completed_trials = [t for t in trials if t.state == optuna.trial.TrialState.COMPLETE]
    incomplete_trials = [t for t in trials if t.state != optuna.trial.TrialState.COMPLETE]
    
    # Convert to DataFrames
    completed_df = study.trials_dataframe().loc[study.trials_dataframe()['state'] == 'COMPLETE'].reset_index(drop=True) if completed_trials else pd.DataFrame()
    incomplete_df = study.trials_dataframe().loc[study.trials_dataframe()['state'] != 'COMPLETE'].reset_index(drop=True) if incomplete_trials else pd.DataFrame()
    
    return completed_df, incomplete_df