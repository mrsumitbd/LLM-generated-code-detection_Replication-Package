import os
import json
from typing import Optional

def get_run_step(step_run_id: str) -> str:
    """Get a run step by name, ID, or prefix.

    Args:
        step_run_id: The ID of the run step to retrieve
    """
    run_steps_dir = os.path.join(os.getcwd(), "run_steps")
    if not os.path.exists(run_steps_dir):
        return "Run step not found"

    for filename in os.listdir(run_steps_dir):
        if filename.startswith(step_run_id):
            with open(os.path.join(run_steps_dir, filename), "r") as f:
                step_data = json.load(f)
            return step_data["name"]

    return "Run step not found"