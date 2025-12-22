import os
import time
from typing import Optional
from dataclasses import dataclass

import wandb
from transformers import Trainer, TrainingArguments
from transformers.integrations import WandbCallback

TRAINING_TIMEOUT = 3600  # 1 hour

@dataclass
class TrainingParamsGr00T:
    num_epochs: int
    learning_rate: float
    batch_size: int
    max_seq_length: int


def train(
    training_id: int,
    dataset_name: str,
    wandb_api_key: Optional[str],
    model_name: str,
    training_params: TrainingParamsGr00T,
    user_hf_token: Optional[str] = None,
    private_mode: bool = False,
    timeout_seconds: int = TRAINING_TIMEOUT,
    wandb_run_id: Optional[str] = None,
    **kwargs,
):
    # Verify input parameters
    assert isinstance(training_id, int) and training_id > 0
    assert isinstance(dataset_name, str) and dataset_name
    assert isinstance(model_name, str) and model_name
    assert isinstance(training_params, TrainingParamsGr00T)
    assert user_hf_token is None or isinstance(user_hf_token, str)
    assert isinstance(private_mode, bool)
    assert isinstance(timeout_seconds, int) and timeout_seconds > 0
    assert wandb_run_id is None or isinstance(wandb_run_id, str)

    # Set up Weights & Biases (WandB) logging
    if wandb_api_key:
        os.environ["WANDB_API_KEY"] = wandb_api_key
        wandb.init(
            project="phosphobot",
            entity="your-wandb-entity",
            name=f"training-{training_id}",
            id=wandb_run_id,
            resume="allow",
            config=training_params.__dict__,
        )

    # Load the model
    model = load_model(model_name, user_hf_token)

    # Prepare the training arguments
    training_args = TrainingArguments(
        output_dir=f"./results/{training_id}",
        num_train_epochs=training_params.num_epochs,
        per_device_train_batch_size=training_params.batch_size,
        learning_rate=training_params.learning_rate,
        max_seq_length=training_params.max_seq_length,
        save_strategy="epoch",
        evaluation_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
    )

    # Create the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=load_dataset(dataset_name, "train", user_hf_token),
        eval_dataset=load_dataset(dataset_name, "validation", user_hf_token),
        callbacks=[WandbCallback()] if wandb_api_key else [],
    )

    # Train the model
    start_time = time.time()
    trainer.train()
    training_duration = time.time() - start_time

    # Save the model
    trainer.save_model(f"./results/{training_id}/model")

    # Log the training duration
    if wandb_api_key:
        wandb.log({"training_duration": training_duration})

    return training_duration