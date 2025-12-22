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
        import torch.distributed as dist
        
        self.max_tokens_per_rank = max_tokens_per_rank
        
        if rank is None:
            self.rank = dist.get_rank()
        else:
            self.rank = rank
            
        if world_size is None:
            self.world_size = dist.get_world_size()
        else:
            self.world_size = world_size
            
        self.dummy_sample = dummy_sample

    def __call__(self, batch: list[dict]):
        from flash_attn.utils.distributed import batch_lengths_to_minibatches_lpt
        from flash_attn.utils.pretrained import mb_collate_fn
        
        # Filter out samples longer than max_tokens_per_rank
        filtered_batch = [sample for sample in batch if sample.get('length', len(sample.get('input_ids', []))) <= self.max_tokens_per_rank]
        
        # Get lengths of filtered samples
        lengths = [sample.get('length', len(sample.get('input_ids', []))) for sample in filtered_batch]
        
        # Determine minibatches using LPT algorithm
        minibatches = batch_lengths_to_minibatches_lpt(
            lengths,
            self.max_tokens_per_rank,
            self.world_size
        )
        
        # Collect samples for current rank across all minibatches
        all_minibatch_samples = []
        
        for minibatch_indices in minibatches:
            rank_samples = []
            
            # minibatch_indices is a list of (rank, sample_idx) tuples
            for rank_idx, sample_idx in minibatch_indices:
                if rank_idx == self.rank:
                    if sample_idx < len(filtered_batch):
                        rank_samples.append(filtered_batch[sample_idx])
                    else:
                        if self.dummy_sample is not None:
                            rank_samples.append(self.dummy_sample)
            
            # Collate samples for this minibatch
            if rank_samples:
                collated = mb_collate_fn(rank_samples)
                all_minibatch_samples.append(collated)
        
        # If no samples for this rank, return empty or dummy
        if not all_minibatch_samples:
            if self.dummy_sample is not None:
                return mb_collate_fn([self.dummy_sample])
            return mb_collate_fn([])
        
        # If single minibatch, return it directly
        if len(all_minibatch_samples) == 1:
            return all_minibatch_samples[0]
        
        # If multiple minibatches, concatenate them
        return all_minibatch_samples