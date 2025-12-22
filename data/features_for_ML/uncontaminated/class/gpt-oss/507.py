import torch

class TeaCache:
    """
    A simple cache for diffusion inference steps that checks whether the current
    hidden states are close enough to the cached ones based on a relative L1
    threshold.  The cache can be updated or stored explicitly.
    """

    def __init__(self, num_inference_steps: int, rel_l1_thresh: float):
        """
        Parameters
        ----------
        num_inference_steps : int
            The total number of inference steps (unused in this simple implementation
            but kept for API compatibility).
        rel_l1_thresh : float
            Relative L1 threshold for deciding if the current hidden states are
            close enough to the cached ones.
        """
        self.num_inference_steps = num_inference_steps
        self.rel_l1_thresh = rel_l1_thresh
        self._cache = None

    def check(self, dit, hidden_states: torch.Tensor, conditioning):
        """
        Check whether the current hidden states are within the relative L1 threshold
        of the cached hidden states.

        Parameters
        ----------
        dit : FluxDiT
            The diffusion model (unused in this simple implementation).
        hidden_states : torch.Tensor
            The current hidden states to compare.
        conditioning : Any
            Conditioning information (unused in this simple implementation).

        Returns
        -------
        bool
            True if the cached hidden states exist and the relative L1 difference
            is below the threshold, False otherwise.
        """
        if self._cache is None:
            return False

        # Compute relative L1 difference
        diff = torch.abs(hidden_states - self._cache)
        l1_diff = diff.sum()
        l1_cache = torch.abs(self._cache).sum()
        # Avoid division by zero
        if l1_cache == 0:
            return l1_diff == 0

        rel_l1 = l1_diff / l1_cache
        return rel_l1 < self.rel_l1_thresh

    def store(self, hidden_states: torch.Tensor):
        """
        Store a copy of the hidden states in the cache.

        Parameters
        ----------
        hidden_states : torch.Tensor
            The hidden states to cache.
        """
        self._cache = hidden_states.clone()

    def update(self, hidden_states: torch.Tensor):
        """
        Update the cached hidden states with a new copy.

        Parameters
        ----------
        hidden_states : torch.Tensor
            The new hidden states to replace the cache.
        """
        self.store(hidden_states)