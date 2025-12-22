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
    """Train for one epoch with deterministic resume support."""
    model.train()
    probe.train()
    
    total_loss = 0.0
    total_samples = 0
    all_preds = []
    all_targets = []
    
    batches_per_epoch = batches_per_epoch or len(train_loader)
    
    for batch_idx, (inputs, targets) in enumerate(train_loader):
        if batch_idx < start_batch:
            continue
        
        if batch_idx >= batches_per_epoch:
            break
        
        inputs = inputs.to(device)
        targets = targets.to(device)
        
        optimizer.zero_grad()
        
        with torch.no_grad():
            features = model(inputs)
        
        logits = probe(features)
        loss = criterion(logits, targets)
        
        loss.backward()
        optimizer.step()
        scheduler.step()
        
        total_loss += loss.item() * inputs.size(0)
        total_samples += inputs.size(0)
        
        with torch.no_grad():
            if hasattr(criterion, '__class__') and 'BCEWithLogitsLoss' in criterion.__class__.__name__:
                preds = torch.sigmoid(logits)
            else:
                preds = torch.softmax(logits, dim=1)
            
            all_preds.append(preds.cpu())
            all_targets.append(targets.cpu())
        
        global_step += 1
        
        if output_dir is not None and (batch_idx + 1) % checkpoint_every == 0:
            checkpoint_path = output_dir / f"checkpoint_epoch{epoch}_batch{batch_idx}.pt"
            torch.save({
                'epoch': epoch,
                'batch': batch_idx,
                'global_step': global_step,
                'model_state_dict': model.state_dict(),
                'probe_state_dict': probe.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
            }, checkpoint_path)
    
    avg_loss = total_loss / total_samples if total_samples > 0 else 0.0
    
    all_preds = torch.cat(all_preds, dim=0)
    all_targets = torch.cat(all_targets, dim=0)
    
    if all_targets.dim() > 1 and all_targets.size(1) > 1:
        all_targets_binary = all_targets
        if all_preds.size(1) > 1:
            all_preds_binary = all_preds
        else:
            all_preds_binary = all_preds
    else:
        all_targets_binary = all_targets
        all_preds_binary = all_preds
    
    try:
        if all_targets_binary.dim() == 1:
            auroc = roc_auc_score(all_targets_binary.numpy(), all_preds_binary.numpy())
        else:
            auroc = roc_auc_score(all_targets_binary.numpy(), all_preds_binary.numpy(), multi_class='ovr')
    except:
        auroc = 0.0
    
    return avg_loss, auroc, global_step