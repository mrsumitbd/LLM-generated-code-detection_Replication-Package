import os
from .helper import train_gr00t_on_modal
from loguru import logger
from supabase import Client, create_client
from datetime import datetime, timezone
from huggingface_hub.errors import (
    HFValidationError,
    RepositoryNotFoundError,
    RevisionNotFoundError,
)
from phosphobot.am.base import TrainingParamsGr00T
from datetime import datetime, timezone
from fastapi import HTTPException
from supabase import Client, create_client

def train(  # All these args should be verified in phosphobot
    training_id: int,
    dataset_name: str,
    wandb_api_key: str | None,
    model_name: str,
    training_params: TrainingParamsGr00T,
    user_hf_token: str | None = None,
    private_mode: bool = False,
    timeout_seconds: int = TRAINING_TIMEOUT,
    wandb_run_id: str | None = None,
    **kwargs,
):
    from datetime import datetime, timezone

    from supabase import Client, create_client

    from .helper import train_gr00t_on_modal

    SUPABASE_URL = os.environ["SUPABASE_URL"]
    SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Use user's HF token for private training, fallback to system token
    hf_token = user_hf_token or os.getenv("HF_TOKEN")

    if hf_token is None:
        raise ValueError(
            "HF_TOKEN is not available (neither user token nor system token)"
        )

    logger.info(
        f"🚀 Training Gr00t on {dataset_name} with id {training_id} and uploading to: {model_name}  (private_mode={private_mode})"
    )

    # Set the wandb run id if it is not set, using the environment variable
    if wandb_run_id:
        logger.info(f"Setting WANDB_RUN_ID to {wandb_run_id}")
        os.environ["WANDB_RUN_ID"] = wandb_run_id

    try:
        train_gr00t_on_modal(
            dataset_repo_id=dataset_name,
            hf_token=hf_token,
            wandb_api_key=wandb_api_key,
            hf_model_name=model_name,
            timeout_seconds=timeout_seconds,
            training_params=training_params,
            private_mode=private_mode,
        )

        logger.info(f"✅ Training {training_id} for {dataset_name} completed")

        terminated_at = datetime.now(timezone.utc).isoformat()

        # Update the training status
        supabase_client.table("trainings").update(
            {
                "status": "succeeded",
                "terminated_at": terminated_at,
                # no logs for now
            }
        ).eq("id", training_id).execute()
    except TimeoutError as e:
        logger.warning(
            "Training timed out—uploading partial checkpoint before failing", exc_info=e
        )
        _upload_partial_checkpoint_gr00t(model_name, hf_token)
        supabase_client.table("trainings").update(
            {
                "status": "failed",
                "terminated_at": datetime.now(timezone.utc).isoformat(),
            }
        ).eq("id", training_id).execute()
        raise e
    except HFValidationError as e:
        logger.warning(f"Validation error during training: {e}")
        # Update the training status in Supabase
        supabase_client.table("trainings").update(
            {
                "status": "failed",
                "terminated_at": datetime.now(timezone.utc).isoformat(),
            }
        ).eq("id", training_id).execute()
        raise HTTPException(
            status_code=400,
            detail=f"HuggingFace validation error: {e}",
        )
    except Exception as e:
        logger.error(f"🚨 Gr00t training {training_id} for {dataset_name} failed: {e}")
        # Update the training status in Supabase
        supabase_client.table("trainings").update(
            {
                "status": "failed",
                "terminated_at": datetime.now(timezone.utc).isoformat(),
            }
        ).eq("id", training_id).execute()
        raise e