import math
from typing import Tuple

def estimate_duration(annflux_state, step_state: Tuple[str, int, int]) -> Tuple[int, int]:
    """
    Estimate duration of state transitions to provide progressbar functionality

    :return (estimated duration in seconds, standard deviation of estimated duration in seconds)
    """
    state_name, current_step_index, total_steps = step_state

    # Retrieve recorded durations for the given state
    durations = None
    if hasattr(annflux_state, "state_durations"):
        # Expecting a dict: {state_name: [durations]}
        durations = annflux_state.state_durations.get(state_name)
    elif hasattr(annflux_state, "get_durations"):
        # Expecting a method that returns a list of durations
        durations = annflux_state.get_durations(state_name)

    if not durations:
        return (0, 0)

    n = len(durations)
    mean = sum(durations) / n
    if n > 1:
        var = sum((x - mean) ** 2 for x in durations) / (n - 1)
        std = math.sqrt(var)
    else:
        std = 0.0

    # Estimate remaining duration based on remaining steps
    remaining = max(total_steps - current_step_index, 0)
    if remaining == 0:
        return (0, 0)

    est_duration = mean * remaining
    est_std = std * math.sqrt(remaining)

    return (int(round(est_duration)), int(round(est_std)))