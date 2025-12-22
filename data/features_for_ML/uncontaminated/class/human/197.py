import torch
import torch.distributed as dist
from mini_trainer.batch_packer import batch_lengths_to_minibatches_lpt
from mini_trainer.utils import log_rank_0

class MaxTokensPerRankCollator:
    """A collate function for PyTorch DataLoader for distributed training.

    This collator takes a batch of samples (obtained using indices from a sampler
    like InfiniteSampler) and performs two main tasks:
    1. Filters out samples longer than `max_tokens_per_rank`.
    2. Uses `batch_lengths_to_minibatches_lpt` to determine how to distribute the
       remaining samples across ranks into one or more 'minibatches', ensuring
       no rank exceeds `max_tokens_per_rank` per minibatch.
    3. For the current rank, it fetches the assigned samples (or dummy samples
       for padding) for each determined minibatch.
    4. Uses `mb_collate_fn` to collate the samples for each minibatch into the
       packed format required by Flash Attention.

    Args:
        max_tokens_per_rank (int): Maximum number of tokens allowed per rank
            in a single processed minibatch.
        rank (int, optional): The rank of the current process. If None, attempts
            to get it from `torch.distributed`.
        world_size (int, optional): Total number of ranks. If None, attempts
            to get it from `torch.distributed`.
        dummy_sample (dict, optional): A sample used for padding when a rank
            has no real samples assigned in a minibatch.
    """
    def __init__(self, max_tokens_per_rank: int, rank: int=None, world_size: int=None, dummy_sample=None):
        self.max_tokens_per_rank = max_tokens_per_rank

        if rank is None:
            self.global_rank = dist.get_rank() if dist.is_available() and dist.is_initialized() else 0
        else:
            self.global_rank = rank
        if world_size is None:
            self.world_size = dist.get_world_size() if dist.is_available() and dist.is_initialized() else 1
        else:
            self.world_size = world_size
        if dummy_sample is None:
            dummy_sample = {'input_ids': torch.tensor([15, 14, 13, 12, 11], dtype=torch.long),
                            'labels': torch.tensor([-100, -100, -100, -100, -100], dtype=torch.long),
                            'len': 5,
                            'num_loss_counted_tokens': 0}
        self.dummy_sample = dummy_sample

    def __call__(self, batch: list[dict]):
        """Processes a batch of samples into a list of packed minibatches for the current rank.

        Args:
            batch: A list of sample dictionaries from the Dataset.

        Returns:
            A list where each element is a dictionary representing a collated minibatch
            (output of `mb_collate_fn`) ready for processing by the current rank.
        """
        batch_ = [b for b in batch if b['len'] <= self.max_tokens_per_rank]
        if len(batch_) < len(batch):
            log_rank_0(f"\033[38;5;196mremoved {len(batch) - len(batch_)} samples from batch because they are longer than the max tokens per gpu\033[0m")
        # Use filtered batch for lengths and loss counts
        batch_lengths = [sample["len"] for sample in batch_]
        batch_num_loss_counted_tokens = sum(
            [sample["num_loss_counted_tokens"] for sample in batch_]
        )
        all_minibatches_indices = batch_lengths_to_minibatches_lpt(
            batch_lengths, self.max_tokens_per_rank, self.world_size, self.global_rank
        )

        all_minibatches = []
        for mb_indices in all_minibatches_indices:
            mb = [batch_[i] if i != -1 else self.dummy_sample for i in mb_indices]
            all_minibatches.append(mb_collate_fn(mb, batch_num_loss_counted_tokens))

        return all_minibatches