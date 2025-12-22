import os
import shutil
import logging
from huggingface_hub import HfApi, HfFolder

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
    try:
        # Find the latest checkpoint in the output directory
        checkpoint_dir = os.path.join(output_dir, "checkpoint")
        if not os.path.exists(checkpoint_dir):
            logging.warning("No checkpoint directory found, skipping upload.")
            return

        latest_checkpoint = max(
            [os.path.join(checkpoint_dir, f) for f in os.listdir(checkpoint_dir)],
            key=os.path.getmtime,
        )

        # Upload the checkpoint to the Hugging Face Hub
        api = HfApi()
        HfFolder.save_token(hf_token)
        api.upload_folder(
            folder_path=latest_checkpoint,
            repo_id=hf_model_name,
            commit_message="Uploading latest checkpoint",
        )
        logging.info(f"Uploaded checkpoint to {hf_model_name}")
    except Exception as e:
        logging.error(f"Error uploading checkpoint: {e}")