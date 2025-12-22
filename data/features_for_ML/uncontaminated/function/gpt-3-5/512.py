def estimate_duration(annflux_state: AnnFluxState, step_state: Tuple[str, int, int]) -> (int, int):
    total_steps = annflux_state.total_steps
    current_step = step_state[1]
    steps_remaining = total_steps - current_step
    time_per_step = annflux_state.total_duration / total_steps
    estimated_duration = steps_remaining * time_per_step
    std_deviation = time_per_step * (steps_remaining ** 0.5)
    return int(estimated_duration), int(std_deviation)