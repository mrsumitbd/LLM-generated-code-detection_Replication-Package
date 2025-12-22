def get_optimization_parameters():
    return {
        "learning_rate": 0.001,
        "batch_size": 32,
        "epochs": 10,
        "optimizer": "adam",
        "loss": "categorical_crossentropy",
        "metrics": ["accuracy"],
        "validation_split": 0.2,
        "callbacks": None,
    }