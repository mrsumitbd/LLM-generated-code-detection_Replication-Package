def get_run_step(step_run_id: str) -> str:
    """Get a run step by name, ID, or prefix.

    Args:
        step_run_id: The ID of the run step to retrieve
    """
    # Attempt to import a global mapping of step names to IDs if available.
    try:
        from . import RUN_STEPS  # type: ignore
    except Exception:
        RUN_STEPS = {}

    # If the mapping is empty, just return the provided identifier.
    if not RUN_STEPS:
        return step_run_id

    # Normalize the input
    step_run_id = step_run_id.strip()

    # 1. If the identifier is a key in the mapping, return its value (the ID).
    if step_run_id in RUN_STEPS:
        return RUN_STEPS[step_run_id]

    # 2. If the identifier is already an ID (i.e., appears in the values), return it.
    if step_run_id in RUN_STEPS.values():
        return step_run_id

    # 3. Treat the identifier as a prefix: find all keys that start with it.
    matches = [name for name in RUN_STEPS if name.startswith(step_run_id)]
    if len(matches) == 1:
        return RUN_STEPS[matches[0]]
    if len(matches) > 1:
        raise ValueError(
            f"Ambiguous prefix '{step_run_id}'. Matches: {', '.join(matches)}"
        )

    # 4. If no matches found, raise an error.
    raise ValueError(f"Run step '{step_run_id}' not found.")