def on_workflow_start(execution_id: str, workflow_id: str, inputs: dict[str, Any]) -> None:
    """
    Called when a workflow execution starts.
    
    Args:
        execution_id: Unique identifier for this workflow execution
        workflow_id: Identifier for the workflow being executed
        inputs: Dictionary of input parameters for the workflow
    """
    import logging
    from datetime import datetime
    
    logger = logging.getLogger(__name__)
    
    logger.info(
        f"Workflow started - execution_id: {execution_id}, "
        f"workflow_id: {workflow_id}, timestamp: {datetime.now().isoformat()}"
    )
    
    if inputs:
        logger.debug(f"Workflow inputs: {inputs}")