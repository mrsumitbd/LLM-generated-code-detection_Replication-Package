import torch
import torch.distributed as dist
from typing import List, Dict, Any, Optional

# These helper functions are assumed to be defined elsewhere in the codebase.
# They should be imported from the appropriate module.
# Replace `your_module` with the actual module name where these functions reside.
try:
    from your_module import batch_lengths_to_minibatches_lpt, mb_collate_fn
except ImportError:
    # If the functions are not available, raise an informative error.
    raise ImportError(
        "batch_lengths_to_minibatches_lpt and mb_collate_fn must be implemented "
        "and importable from your_module."
    )


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

    def __init__(
        self,
        max_tokens_per_rank: int,
        rank: Optional[int] = None,
        world_size: Optional[int] = None,
        dummy_sample: Optional[Dict[str, Any]] = None,
    ):
        self.max_tokens_per_rank = max_tokens_per_rank

        if rank is None:
            if not dist.is_available() or not dist.is_initialized():
                raise RuntimeError(
                    "Distributed package is not available or not initialized. "
                    "Please provide `rank` explicitly."
                )
            self.rank = dist.get_rank()
        else:
            self.rank = rank

        if world_size is None:
            if not dist.is_available() or not dist.is_initialized():
                raise RuntimeError(
                    "Distributed package is not available or not initialized. "
                    "Please provide `world_size` explicitly."
                )
            self.world_size = dist.get_world_size()
        else:
            self.world_size = world_size

        self.dummy_sample = dummy_sample

    def __call__(self, batch: List[Dict[str, Any]]) -> List[Any]:
        """
        Collate a batch of samples for the current rank.

        Parameters
        ----------
        batch : List[Dict[str, Any]]
            A list of samples, each sample is a dictionary containing at least
            a 'tokens' key (or any key that can be used to determine the length).

        Returns
        -------
        List[Any]
            A list of collated minibatches for the current rank. Each element
            is the result of `mb_collate_fn` applied to the samples belonging
            to that minibatch.
        """
        # 1. Filter out samples longer than max_tokens_per_rank
        filtered_samples = []
        lengths = []

        for sample in batch:
            # Determine the length of the sample
            tokens = sample.get("tokens")
            if tokens is None:
                raise KeyError("Each sample must contain a 'tokens' key.")
            if isinstance(tokens, torch.Tensor):
                length = tokens.shape[0]
            else:
                length = len(tokens)

            if length <= self.max_tokens_per_rank:
                filtered_samples.append(sample)
                lengths.append(length)

        # If no samples remain after filtering, return a single dummy minibatch
        if not filtered_samples:
            if self.dummy_sample is None:
                # Return an empty list if no dummy sample is provided
                return []
            # Collate a single dummy minibatch
            return [mb_collate_fn([self.dummy_sample])]

        # 2. Determine minibatch assignments across ranks
        # The helper function is expected to return a list of minibatches,
        # where each minibatch is a list of indices for each rank.
        # Example: minibatches = [[rank0_indices], [rank1_indices], ...]
        minibatches = batch_lengths_to_minibatches_lpt(
            lengths, self.max_tokens_per_rank, self.world_size
        )

        # 3. For the current rank, fetch assigned samples for each minibatch
        collated_minibatches = []
        for mb_indices in minibatches:
            # mb_indices should be a list of indices for each rank
            if not isinstance(mb_indices, (list, tuple)):
                raise TypeError(
                    "Expected minibatch indices to be a list or tuple per rank."
                )
            if self.rank >= len(mb_indices):
                # If the rank index is out of bounds, treat as empty
                indices_for_rank = []
            else:
                indices_for_rank = mb_indices[self.rank]

            # Map indices to actual samples
            if indices_for_rank:
                samples_for_rank = [filtered_samples[i] for i in indices_for_rank]
            else:
                # Use dummy sample for padding if provided
                if self.dummy_sample is None:
                    samples_for_rank = []
                else:
                    samples_for_rank = [self.dummy_sample]

            # 4. Collate the samples for this minibatch
            collated = mb_collate_fn(samples_for_rank)
            collated_minibatches.append(collated)

        return collated_minibatches