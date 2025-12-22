def get_run_step(step_run_id: str) -> str:
    """Get a run step by name, ID, or prefix.

    Args:
        step_run_id: The ID of the run step to retrieve
    """
    run_step = get_zenml_client().get_run_step(step_run_id)
    return run_step.model_dump_json()