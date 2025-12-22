import os

def get_cfgs():
    """
    Return a dictionary of configuration parameters.
    Values can be overridden by environment variables.
    """
    cfg = {
        "learning_rate": float(os.getenv("LEARNING_RATE", 0.001)),
        "batch_size": int(os.getenv("BATCH_SIZE", 32)),
        "num_epochs": int(os.getenv("NUM_EPOCHS", 10)),
        "model_name": os.getenv("MODEL_NAME", "default_model"),
    }
    return cfg