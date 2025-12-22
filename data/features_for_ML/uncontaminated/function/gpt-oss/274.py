import os
import re
import logging
from typing import Optional

try:
    from huggingface_hub import upload_folder
except ImportError:
    upload_folder = None  # pragma: no cover


def _upload_partial_checkpoint_gr00t(
    hf_model_name: str,
    hf_token: str,
    output_dir: str = "/tmp/outputs/train",
) -> None:
    """
    Uploads the latest checkpoint from a timed-out Gr00t training run
    to the Hugging Face Hub model repo. Fails safely if no checkpoints
    are found or an upload error occurs.
    """
    logger = logging.getLogger(__name__)

    if upload_folder is None:
        logger.warning("huggingface_hub is not installed; cannot upload checkpoints.")
        return

    if not os.path.isdir(output_dir):
        logger.warning(f"Output directory {output_dir!r} does not exist.")
        return

    # Find all checkpoint directories (e.g., "checkpoint-1234")
    checkpoint_pattern = re.compile(r"^checkpoint-(\d+)$")
    checkpoints = []
    for entry in os.listdir(output_dir):
        match = checkpoint_pattern.match(entry)
        if match and os.path.isdir(os.path.join(output_dir, entry)):
            checkpoints.append((int(match.group(1)), entry))

    if not checkpoints:
        logger.info("No checkpoint directories found in %s.", output_dir)
        return

    # Pick the checkpoint with the highest step number
    _, latest_checkpoint_name = max(checkpoints, key=lambda x: x[0])
    latest_checkpoint_path = os.path.join(output_dir, latest_checkpoint_name)

    logger.info(
        "Uploading latest checkpoint %s to Hugging Face Hub repo %s",
        latest_checkpoint_path,
        hf_model_name,
    )

    try:
        upload_folder(
            local_dir=latest_checkpoint_path,
            repo_id=hf_model_name,
            token=hf_token,
            path_in_repo="checkpoints",
            repo_type="model",
            commit_message=f"Upload checkpoint {latest_checkpoint_name}",
        )
        logger.info("Checkpoint upload succeeded.")
    except Exception as exc:  # pragma: no cover
        logger.error(
            "Failed to upload checkpoint %s to Hugging Face Hub: %s",
            latest_checkpoint_path,
            exc,
        )