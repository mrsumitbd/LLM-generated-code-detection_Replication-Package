from datetime import datetime
import torch
from sklearn.metrics import roc_auc_score
from torch.utils.data import DataLoader, Subset
import json
from tqdm import tqdm
from pathlib import Path
from torch.optim.lr_scheduler import OneCycleLR
import torch.nn as nn

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
    probe.train()

    total_loss = 0
    all_preds = []
    all_labels = []
    batches_processed = 0
    samples_seen = 0  # Track actual samples processed
    current_auroc = 0.5  # Initialize to avoid NameError

    pbar = tqdm(train_loader, desc=f"Epoch {epoch}")

    for batch_idx, (x, y) in enumerate(pbar):
        # Skip already-processed batches when resuming mid-epoch
        if batch_idx < start_batch:
            continue

        x, y = x.to(device), y.to(device)
        samples_seen += x.size(0)  # Track actual batch size

        # Log first batch shapes for diagnostics
        if batch_idx == 0 and epoch == 0:
            logger.info(f"First batch - x.shape: {x.shape}, y.dtype: {y.dtype}, y.shape: {y.shape}")

        # Extract EEGPT features (frozen backbone)
        with torch.no_grad():
            features = model.extract_features(x, summary=False)  # (B, 4, 512)
            features = features.flatten(1)  # match original behavior

        # Forward through probe
        logits = probe(features).squeeze(-1)  # (B,)

        # Compute loss
        loss = criterion(logits, y)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # BULLETPROOF scheduler step using internal counters
        try:
            # OneCycleLR tracks its own step count internally
            total_steps = getattr(scheduler, "total_steps", None)
            step_count = getattr(scheduler, "_step_count", None)

            # Only step if we haven't reached the limit
            if total_steps is None or step_count is None or step_count < total_steps:
                scheduler.step()
            else:
                logger.debug(f"Scheduler at limit: {step_count}/{total_steps}, skipping step")
        except (ValueError, RuntimeError) as e:
            # This should never happen with the guard above, but just in case
            logger.warning(f"Scheduler step skipped at batch {batch_idx + start_batch}: {e}")

        # Increment global step AFTER successful scheduler step
        global_step += 1

        # Track metrics
        total_loss += loss.item()
        batches_processed += 1
        preds = torch.sigmoid(logits).detach().cpu().numpy()
        all_preds.extend(preds)
        all_labels.extend(y.cpu().numpy())

        # Update progress bar
        if batch_idx % 10 == 0:
            current_auroc = (
                roc_auc_score(all_labels, all_preds) if len(set(all_labels)) > 1 else 0.5
            )
            pbar.set_postfix(
                {
                    'loss': f'{loss.item():.4f}',
                    'auroc': f'{current_auroc:.4f}',
                    'lr': f'{scheduler.get_last_lr()[0]:.6f}',
                }
            )

        # Write heartbeat for monitoring
        if output_dir and batch_idx % 50 == 0:
            batch_size = x.shape[0]  # Actual batch size from data
            heartbeat = {
                'timestamp': datetime.now().isoformat(),
                'epoch': epoch,
                'batch_idx': batch_idx + start_batch,  # Report absolute batch index
                'total_batches': batches_per_epoch
                or (len(train_loader) + start_batch),  # Exact if provided
                'loss': float(loss.item()),
                'auroc': float(current_auroc) if 'current_auroc' in locals() else 0.5,
                'lr': float(scheduler.get_last_lr()[0]),
                'global_step': global_step,
                'samples_seen': samples_seen,
                'gpu_memory_gb': torch.cuda.memory_allocated() / 1e9
                if torch.cuda.is_available()
                else 0,
                'alive': True,
            }
            heartbeat_file = output_dir / 'heartbeat.json'
            with open(heartbeat_file, 'w') as f:
                json.dump(heartbeat, f, indent=2)
            # Also refresh a rolling 'checkpoint_latest.pt' to minimize loss on crash
            try:
                latest_ckpt = {
                    'epoch': epoch,
                    'batch_idx': batch_idx + start_batch,
                    'probe_state_dict': probe.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'scheduler_state_dict': scheduler.state_dict(),
                    'best_auroc': best_auroc,
                    'global_step': global_step,
                    'epoch_indices': epoch_indices,
                }
                torch.save(latest_ckpt, (output_dir / 'checkpoint_latest.pt'))
            except Exception:
                pass

        # CRITICAL: Save checkpoint every N batches to avoid losing progress
        # Use absolute batch index for uniform intervals across restarts
        abs_batch_idx = batch_idx + start_batch
        if (
            output_dir
            and checkpoint_every
            and abs_batch_idx > 0
            and abs_batch_idx % checkpoint_every == 0
        ):
            checkpoint = {
                'epoch': epoch,
                'batch_idx': batch_idx + start_batch,  # Save absolute batch index
                'probe_state_dict': probe.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'best_auroc': best_auroc,
                'train_loss': total_loss / batches_processed if batches_processed > 0 else 0,
                'global_step': global_step,
                'epoch_indices': epoch_indices,  # Save deterministic order
                'sample_offset': samples_seen,  # Exact samples processed (using actual counter)
            }
            checkpoint_path = (
                output_dir / f'checkpoint_epoch{epoch}_batch{batch_idx + start_batch}.pt'
            )
            torch.save(checkpoint, checkpoint_path)
            logger.info(
                f"Saved intra-epoch checkpoint at epoch {epoch}, batch {batch_idx + start_batch}"
            )

    # Calculate epoch metrics
    avg_loss = total_loss / batches_processed if batches_processed > 0 else 0
    epoch_auroc = (
        roc_auc_score(all_labels, all_preds)
        if len(set(all_labels)) > 1 and len(all_labels) > 0
        else 0.5
    )

    return avg_loss, epoch_auroc, global_step