def estimate_duration(annflux_state: AnnFluxState, step_state: Tuple[str, int, int]) -> (int, int):
    """
    Estimate duration of state transitions to provide progressbar functionality

    :return (estimated duration in seconds, standard deviation of estimated duration in seconds)
    """
    step_name, current_step, total_steps = step_state
    if step_name == "Preprocessing":
        estimated_duration = 60 * (total_steps - current_step)
        std_dev = 10
    elif step_name == "Training":
        estimated_duration = 120 * (total_steps - current_step)
        std_dev = 20
    elif step_name == "Evaluation":
        estimated_duration = 30 * (total_steps - current_step)
        std_dev = 5
    else:
        estimated_duration = 0
        std_dev = 0
    return estimated_duration, std_dev