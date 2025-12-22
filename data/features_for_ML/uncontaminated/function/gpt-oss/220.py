import os
import time
import signal
from typing import Any, Dict, Optional

import datasets
import torch
import wandb
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

# Constants that are expected to be defined elsewhere in the project
TRAINING_TIMEOUT = 3600  # default timeout in seconds


def _timeout_handler(signum, frame):
    raise TimeoutError("Training timed out")


def train(
    training_id: int,
    dataset_name: str,
    wandb_api_key: Optional[str],
    model_name: str,
    training_params: Any,
    user_hf_token: Optional[str] = None,
    private_mode: bool = False,
    timeout_seconds: int = TRAINING_TIMEOUT,
    wandb_run_id: Optional[str] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Train a Hugging Face model on a specified dataset.

    Parameters
    ----------
    training_id : int
        Unique identifier for the training run.
    dataset_name : str
        Name of the dataset to load from the Hugging Face Hub.
    wandb_api_key : str | None
        API key for Weights & Biases. If None, wandb is not used.
    model_name : str
        Name of the pretrained model to fine‑tune.
    training_params : TrainingParamsGr00T
        Object containing training hyper‑parameters.
    user_hf_token : str | None
        Hugging Face token for private datasets/models.
    private_mode : bool
        If True, the dataset/model is treated as private.
    timeout_seconds : int
        Maximum allowed training time in seconds.
    wandb_run_id : str | None
        Existing wandb run ID to resume.
    **kwargs
        Additional keyword arguments.

    Returns
    -------
    dict
        Dictionary containing training metadata and metrics.
    """
    # ------------------------------------------------------------------
    # 1. Setup environment
    # ------------------------------------------------------------------
    if wandb_api_key:
        os.environ["WANDB_API_KEY"] = wandb_api_key
        wandb.init(
            project="phosphobot-training",
            id=wandb_run_id,
            resume="must" if wandb_run_id else None,
            config={
                "training_id": training_id,
                "dataset_name": dataset_name,
                "model_name": model_name,
                **training_params.__dict__,
            },
        )

    # ------------------------------------------------------------------
    # 2. Load dataset
    # ------------------------------------------------------------------
    hf_kwargs = {}
    if user_hf_token:
        hf_kwargs["use_auth_token"] = user_hf_token
    if private_mode:
        hf_kwargs["private"] = True

    raw_datasets = datasets.load_dataset(dataset_name, **hf_kwargs)

    # ------------------------------------------------------------------
    # 3. Tokenizer & preprocessing
    # ------------------------------------------------------------------
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=training_params.max_seq_length,
        )

    tokenized_datasets = raw_datasets.map(
        tokenize_function,
        batched=True,
        remove_columns=raw_datasets["train"].column_names,
    )

    # ------------------------------------------------------------------
    # 4. Model
    # ------------------------------------------------------------------
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=training_params.num_labels,
    )

    # ------------------------------------------------------------------
    # 5. Training arguments
    # ------------------------------------------------------------------
    training_args = TrainingArguments(
        output_dir=f"outputs/{training_id}",
        evaluation_strategy="epoch",
        learning_rate=training_params.learning_rate,
        per_device_train_batch_size=training_params.per_device_train_batch_size,
        per_device_eval_batch_size=training_params.per_device_eval_batch_size,
        num_train_epochs=training_params.num_train_epochs,
        weight_decay=training_params.weight_decay,
        logging_dir=f"logs/{training_id}",
        logging_steps=training_params.logging_steps,
        report_to=["wandb"] if wandb_api_key else [],
        run_name=f"train_{training_id}",
        disable_tqdm=False,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
    )

    # ------------------------------------------------------------------
    # 6. Trainer
    # ------------------------------------------------------------------
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets.get("validation"),
        tokenizer=tokenizer,
    )

    # ------------------------------------------------------------------
    # 7. Timeout handling
    # ------------------------------------------------------------------
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout_seconds)

    try:
        # ------------------------------------------------------------------
        # 8. Train
        # ------------------------------------------------------------------
        train_result = trainer.train()
        trainer.save_model(f"outputs/{training_id}/final_model")
        metrics = train_result.metrics
        metrics["training_id"] = training_id
        metrics["dataset_name"] = dataset_name
        metrics["model_name"] = model_name
        metrics["status"] = "completed"
    except TimeoutError:
        metrics = {
            "training_id": training_id,
            "status": "timeout",
            "error": f"Training exceeded {timeout_seconds} seconds",
        }
    finally:
        signal.alarm(0)  # cancel alarm

    # ------------------------------------------------------------------
    # 9. Log to wandb
    # ------------------------------------------------------------------
    if wandb_api_key:
        wandb.log(metrics)
        wandb.finish()

    return metrics