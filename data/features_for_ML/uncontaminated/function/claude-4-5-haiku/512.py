def estimate_duration(annflux_state: AnnFluxState, step_state: Tuple[str, int, int]) -> (int, int):
    """
    Estimate duration of state transitions to provide progressbar functionality

    :return (estimated duration in seconds, standard deviation of estimated duration in seconds)
    """
    state_name, current_step, total_steps = step_state
    
    if not hasattr(annflux_state, 'step_times') or not annflux_state.step_times:
        return (0, 0)
    
    step_times = annflux_state.step_times
    
    if len(step_times) < 2:
        return (0, 0)
    
    # Calculate time differences between consecutive steps
    time_diffs = []
    for i in range(1, len(step_times)):
        diff = step_times[i] - step_times[i-1]
        if diff > 0:
            time_diffs.append(diff)
    
    if not time_diffs:
        return (0, 0)
    
    # Calculate average time per step
    avg_time = sum(time_diffs) / len(time_diffs)
    
    # Calculate standard deviation
    if len(time_diffs) > 1:
        variance = sum((t - avg_time) ** 2 for t in time_diffs) / len(time_diffs)
        std_dev = variance ** 0.5
    else:
        std_dev = 0
    
    # Estimate remaining duration
    remaining_steps = total_steps - current_step
    estimated_duration = int(avg_time * remaining_steps)
    estimated_std_dev = int(std_dev * (remaining_steps ** 0.5))
    
    return (estimated_duration, estimated_std_dev)