def train(args):
    """
    Train a model using the Accelerate library.

    Parameters
    ----------
    args : argparse.Namespace or similar
        Must contain at least the following attributes:
            - model: torch.nn.Module
            - optimizer: torch.optim.Optimizer
            - train_loader: Iterable of training batches
            - val_loader: Iterable of validation batches (optional)
            - epochs: int, number of training epochs
            - checkpoint_path: str, path to save the best model (optional)
            - scheduler: torch.optim.lr_scheduler (optional)
    """
    import torch
    from accelerate import Accelerator

    # Initialize the accelerator
    accelerator = Accelerator()

    # Prepare model, optimizer, data loaders, and scheduler for distributed training
    prepared = [args.model, args.optimizer, args.train_loader, args.val_loader]
    if hasattr(args, "scheduler") and args.scheduler is not None:
        prepared.append(args.scheduler)
    model, optimizer, train_loader, val_loader, *rest = accelerator.prepare(*prepared)
    scheduler = rest[0] if rest else None

    best_val_loss = float("inf")

    for epoch in range(args.epochs):
        model.train()
        for batch in train_loader:
            optimizer.zero_grad()

            # Support both dict and tuple inputs
            if isinstance(batch, dict):
                outputs = model(**batch)
            else:
                outputs = model(*batch)

            # Compute loss
            loss = getattr(outputs, "loss", None)
            if loss is None:
                # Assume the first element is the loss if outputs is a tuple
                loss = outputs[0] if isinstance(outputs, (tuple, list)) else outputs

            accelerator.backward(loss)
            optimizer.step()
            if scheduler is not None:
                scheduler.step()

        # Validation
        if val_loader is not None:
            model.eval()
            val_loss = 0.0
            with torch.no_grad():
                for batch in val_loader:
                    if isinstance(batch, dict):
                        outputs = model(**batch)
                    else:
                        outputs = model(*batch)

                    loss = getattr(outputs, "loss", None)
                    if loss is None:
                        loss = outputs[0] if isinstance(outputs, (tuple, list)) else outputs
                    val_loss += loss.item()
            val_loss /= len(val_loader)

            # Save best model
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                if hasattr(args, "checkpoint_path") and args.checkpoint_path:
                    accelerator.save_state(args.checkpoint_path)

    return model