from pathlib import Path
from loguru import logger
from huggingface_hub import HfApi

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
    hf_api = HfApi(token=hf_token)
    od = Path(output_dir)

    # Find checkpoint-* directories
    try:
        ckpts = sorted(
            [
                d
                for d in od.iterdir()
                if d.is_dir() and d.name.startswith("checkpoint-")
            ],
            key=lambda d: int(d.name.split("-", 1)[1]),
        )
    except FileNotFoundError:
        logger.error(f"Output directory not found: {output_dir}.")
        return

    if not ckpts:
        directories = ", ".join(d.name for d in od.iterdir() if d.is_dir())
        logger.warning(
            f"No checkpoint directories found in {output_dir}, skipping upload. Found directories: {directories}"
        )
        return

    latest = ckpts[-1]
    logger.warning(f"Uploading partial checkpoint: {latest.name}")

    # Upload all files under latest checkpoint
    uploaded_any = False
    for file in latest.rglob("*"):
        if not file.is_file():
            continue
        rel_path = file.relative_to(od)
        try:
            logger.debug(f"→ uploading {file} as {rel_path}")
            hf_api.upload_file(
                repo_id=hf_model_name,
                repo_type="model",
                path_or_fileobj=str(file),
                path_in_repo=str(rel_path),
                token=hf_token,
            )
            uploaded_any = True
        except Exception as e:
            logger.error(f"Failed to upload {rel_path}: {e}")

    if uploaded_any:
        logger.success(f"Partial checkpoint {latest.name} uploaded to {hf_model_name}")
    else:
        logger.warning(f"No files were uploaded for checkpoint {latest.name}")