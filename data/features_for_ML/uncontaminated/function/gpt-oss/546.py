import torch
from torch import nn
from torch.optim import Optimizer
from torch.optim.lr_scheduler import OneCycleLR
from torch.utils.data import DataLoader
from pathlib import Path
from typing import Tuple, Optional, Union
from itertools import islice
from sklearn.metrics import roc_auc_score
import json


def train_epoch(
    model: nn.Module,
    probe: nn.Module,
    train_loader: DataLoader,
    optimizer: Optimizer,
    scheduler: OneCycleLR,
    criterion: nn.Module,
    device: torch.device,
    epoch: int,
    output_dir: Optional[Path] = None,
    checkpoint_every: int = 500,
    best_auroc: float = 0.0,
    start_batch: int = 0,
    global_step: int = 0,
    epoch_indices: Optional[torch.Tensor] = None,
    batches_per_epoch: Optional[int] = None,
) -> Tuple[float, float, int]:
    """
    Train for one epoch with deterministic resume support.

    Parameters
    ----------
    model : nn.Module
        Feature extractor or backbone.
    probe : nn.Module
        Classification head.
    train_loader : DataLoader
        Iterable over training data.
    optimizer : Optimizer
        Optimizer for model + probe parameters.
    scheduler : OneCycleLR
        Learning rate scheduler.
    criterion : nn.Module
        Loss function.
    device : torch.device
        Device to run training on.
    epoch : int
        Current epoch number.
    output_dir : Path | None
        Directory to save checkpoints.
    checkpoint_every : int
        Save checkpoint every N global steps.
    best_auroc : float
        Best AUROC seen so far (used for checkpoint naming).
    start_batch : int
        Batch index to resume from.
    global_step : int
        Global step counter to resume from.
    epoch_indices : torch.Tensor | None
        Optional tensor of indices for each batch (ignored here).
    batches_per_epoch : int | None
        Optional number of batches per epoch (ignored here).

    Returns
    -------
    Tuple[float, float, int]
        Average loss, AUROC for the epoch, and updated global step.
    """
    model.train()
    probe.train()

    # Accumulators
    epoch_loss = 0.0
    all_logits = []
    all_targets = []

    # Prepare iterator that starts at start_batch
    loader_iter = islice(train_loader, start_batch, None)
    for batch_idx, batch in enumerate(loader_iter, start=start_batch):
        # Unpack batch (assumes (inputs, targets))
        inputs, targets = batch
        inputs = inputs.to(device)
        targets = targets.to(device)

        # Forward pass
        optimizer.zero_grad()
        features = model(inputs)
        logits = probe(features)

        # Loss
        loss = criterion(logits, targets)
        loss.backward()
        optimizer.step()
        scheduler.step()

        # Accumulate loss
        epoch_loss += loss.item()

        # Store predictions and targets for AUROC
        with torch.no_grad():
            probs = torch.sigmoid(logits).cpu()
            all_logits.append(probs)
            all_targets.append(targets.cpu())

        # Update global step
        global_step += 1

        # Checkpointing
        if output_dir is not None and global_step % checkpoint_every == 0:
            ckpt_path = output_dir / f"ckpt_epoch{epoch}_step{global_step}.pt"
            ckpt_state = {
                "epoch": epoch,
                "global_step": global_step,
                "model_state_dict": model.state_dict(),
                "probe_state_dict": probe.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "scheduler_state_dict": scheduler.state_dict(),
                "best_auroc": best_auroc,
            }
            torch.save(ckpt_state, ckpt_path)

    # Compute average loss
    num_batches = max(1, batch_idx - start_batch + 1)
    avg_loss = epoch_loss / num_batches

    # Compute AUROC
    if all_logits:
        logits_cat = torch.cat(all_logits, dim=0).numpy()
        targets_cat = torch.cat(all_targets, dim=0).numpy()
        try:
            auroc = roc_auc_score(targets_cat, logits_cat)
        except ValueError:
            # Handle case where only one class present
            auroc = float("nan")
    else:
        auroc = float("nan")

    return avg_loss, auroc, global_step