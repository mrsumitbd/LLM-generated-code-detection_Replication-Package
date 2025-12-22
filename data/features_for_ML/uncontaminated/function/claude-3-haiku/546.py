def train_epoch(
    model: nn.Module,
    probe: nn.Module,
    train_loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    scheduler: OneCycleLR,
    criterion: nn.Module,
    device: torch.device,
    epoch: int,
    output_dir: Path | None = None,
    checkpoint_every: int = 500,
    best_auroc: float = 0.0,
    start_batch: int = 0,
    global_step: int = 0,
    epoch_indices: torch.Tensor | None = None,
    batches_per_epoch: int | None = None,
) -> tuple[float, float, int]:
    model.train()
    probe.train()

    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    if epoch_indices is None:
        epoch_indices = torch.arange(len(train_loader))

    if batches_per_epoch is None:
        batches_per_epoch = len(train_loader)

    for i, batch_idx in enumerate(epoch_indices[start_batch:]):
        inputs, targets = next(iter(train_loader))
        inputs, targets = inputs.to(device), targets.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        probe_outputs = probe(outputs)
        loss = criterion(probe_outputs, targets)
        loss.backward()
        optimizer.step()
        scheduler.step()

        total_loss += loss.item()
        total_correct += (probe_outputs.argmax(dim=1) == targets).sum().item()
        total_samples += targets.size(0)

        global_step += 1

        if (i + start_batch) % checkpoint_every == 0:
            if output_dir is not None:
                torch.save(
                    {
                        "model_state_dict": model.state_dict(),
                        "probe_state_dict": probe.state_dict(),
                        "optimizer_state_dict": optimizer.state_dict(),
                        "scheduler_state_dict": scheduler.state_dict(),
                        "epoch": epoch,
                        "global_step": global_step,
                        "best_auroc": best_auroc,
                    },
                    output_dir / f"checkpoint_epoch_{epoch}_batch_{i + start_batch}.pth",
                )

    train_loss = total_loss / batches_per_epoch
    train_acc = total_correct / total_samples

    return train_loss, train_acc, global_step