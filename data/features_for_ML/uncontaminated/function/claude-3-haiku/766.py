import os
from pathlib import Path
from typing import Dict

from swebench.progress import RunBatchProgressManager

def process_instance(
    instance: dict,
    output_dir: Path,
    config: dict,
    progress_manager: RunBatchProgressManager,
) -> None:
    """Process a single SWEBench instance."""
    instance_id = instance["id"]
    instance_dir = output_dir / str(instance_id)
    instance_dir.mkdir(parents=True, exist_ok=True)

    # Process the instance and save the results
    results = _process_instance(instance, config)
    _save_results(instance_dir, results)

    # Update the progress manager
    progress_manager.update_progress(instance_id)

def _process_instance(instance: dict, config: dict) -> Dict[str, any]:
    # Implement the logic to process the instance and return the results
    # ...
    return {"result1": 42, "result2": "hello"}

def _save_results(instance_dir: Path, results: Dict[str, any]) -> None:
    # Implement the logic to save the results to the instance directory
    # ...
    results_file = instance_dir / "results.json"
    with results_file.open("w") as f:
        json.dump(results, f)