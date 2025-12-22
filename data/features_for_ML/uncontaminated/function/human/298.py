import json
from typing import Any

def on_workflow_start(execution_id: str, workflow_id: str, inputs: dict[str, Any]) -> None:
            logger.debug(f"\n=== Starting workflow: {workflow_id} ===")
            logger.debug(f"Inputs: {json.dumps(inputs, indent=2)}")