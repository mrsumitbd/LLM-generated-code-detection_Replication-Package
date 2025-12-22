def train(
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
    pass