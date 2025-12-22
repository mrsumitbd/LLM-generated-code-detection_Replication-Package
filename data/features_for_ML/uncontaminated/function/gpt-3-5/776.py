def create_optimizer(
    model: TrainableDecoder,
    learning_rate: float,
    betas: tuple[float, float],
    weight_decay: float,
):
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=learning_rate,
        betas=betas,
        weight_decay=weight_decay
    )
    return optimizer