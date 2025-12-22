import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import OneCycleLR
from pathlib import Path

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
    correct = 0
    total = 0
    
    for batch_idx, (inputs, targets) in enumerate(train_loader):
        if batch_idx < start_batch:
            continue
        
        inputs, targets = inputs.to(device), targets.to(device)
        
        optimizer.zero_grad()
        
        outputs = model(inputs)
        outputs = probe(outputs)
        
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        scheduler.step()
        
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
        
        global_step += 1
        
        if epoch_indices is not None:
            epoch_indices[batch_idx] = global_step
        
        if batches_per_epoch is not None and batch_idx >= batches_per_epoch:
            break
        
        if batch_idx % checkpoint_every == 0 and output_dir is not None:
            torch.save({
                'epoch': epoch,
                'batch_idx': batch_idx,
                'model_state_dict': model.state_dict(),
                'probe_state_dict': probe.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'best_auroc': best_auroc,
                'total_loss': total_loss,
                'correct': correct,
                'total': total,
                'global_step': global_step,
                'epoch_indices': epoch_indices,
                'batches_per_epoch': batches_per_epoch
            }, output_dir / f'checkpoint_epoch_{epoch}_batch_{batch_idx}.pth')
    
    return total_loss, correct / total, global_step