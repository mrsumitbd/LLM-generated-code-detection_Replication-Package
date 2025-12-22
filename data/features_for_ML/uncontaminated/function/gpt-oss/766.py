import json
from pathlib import Path
from typing import Dict

def process_instance(
    instance: dict,
    output_dir: Path,
    config: dict,
    progress_manager,
) -> None:
    """
    Process a single SWEBench instance.

    The function writes a JSON file containing the original instance data
    together with a dummy `output` field.  The file is named after the
    instance's `id` field and is stored in `output_dir`.  After writing
    the file, the progress manager is notified that the instance has
    been processed.

    Parameters
    ----------
    instance : dict
        The instance dictionary.  It must contain an `id` key.
    output_dir : Path
        Directory where the output file will be written.
    config : dict
        Configuration dictionary (currently unused but kept for API
        compatibility).
    progress_manager : object
        An object that implements an `update(instance_id, status)`
        method.  The method is called with the instance id and the
        status string ``"completed"``.
    """
    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine the output file name
    instance_id = instance.get("id")
    if instance_id is None:
        raise ValueError("Instance dictionary must contain an 'id' key")

    output_path = output_dir / f"{instance_id}.json"

    # Prepare the data to write
    output_data = {
        "instance": instance,
        "config": config,
        "output": "dummy",  # placeholder for actual model output
    }

    # Write the JSON file
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    # Notify the progress manager
    try:
        progress_manager.update(instance_id, "completed")
    except Exception:
        # If the progress manager does not support update, ignore
        pass