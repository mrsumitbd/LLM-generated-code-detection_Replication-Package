def dump_state(state, label: str = "Current Execution State"):
    """
    Helper method to dump the current state for debugging

    Args:
        state: Execution state to dump
        label: Optional label for the state dump
    """
    logger.debug(f"=== {label} ===")
    logger.debug(f"Workflow ID: {state.workflow_id}")
    logger.debug(f"Current Step ID: {state.current_step_id}")
    logger.debug(f"Inputs: {state.inputs}")
    logger.debug("Step Outputs:")
    for step_id, outputs in state.step_outputs.items():
        logger.debug(f"  {step_id}: {outputs}")
    logger.debug(f"Workflow Outputs: {state.workflow_outputs}")
    logger.debug(f"Status: {state.status}")