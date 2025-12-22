import logging
from typing import Any, Dict

# Configure a basic logger for the workflow system
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("workflow")

def on_workflow_start(execution_id: str, workflow_id: str, inputs: Dict[str, Any]) -> None:
    """
    Called when a workflow starts. Logs the start event and stores the execution context
    in an in-memory registry for later reference.

    Parameters
    ----------
    execution_id : str
        Unique identifier for this execution instance.
    workflow_id : str
        Identifier of the workflow definition being executed.
    inputs : dict[str, Any]
        Dictionary of input parameters for the workflow.
    """
    # Basic validation
    if not execution_id or not workflow_id:
        logger.error("Execution ID and Workflow ID must be provided.")
        return

    # Log the start of the workflow
    logger.info(
        f"Workflow started: execution_id={execution_id}, workflow_id={workflow_id}, inputs={inputs}"
    )

    # Store the execution context in a global registry (optional)
    # This registry can be used by other parts of the system to track running workflows.
    _execution_registry[execution_id] = {
        "workflow_id": workflow_id,
        "inputs": inputs,
        "status": "running",
    }

# Global registry for active executions (simple in-memory store)
_execution_registry: Dict[str, Dict[str, Any]] = {}