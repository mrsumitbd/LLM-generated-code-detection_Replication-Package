import torch
import torch.distributed as dist
from typing import List, Any


class FastAllGatherContext:
    """
    A lightweight context for performing fast all‑gather operations across
    multiple ranks. The context keeps a pre‑allocated buffer that can be
    reused for each gather to reduce memory churn.
    """

    def __init__(
        self,
        rank: int,
        node: int,
        num_ranks: int,
        num_nodes: int,
        max_buffer_size: int = 2 * 32 * 1024 * 1024,
    ):
        self.rank = rank
        self.node = node
        self.num_ranks = num_ranks
        self.num_nodes = num_nodes
        self.max_buffer_size = max_buffer_size

        # Pre‑allocate a byte buffer that can hold the largest expected tensor.
        # The buffer is stored on the CPU to avoid device‑to‑device copies.
        self._buffer = torch.empty(
            (self.max_buffer_size,), dtype=torch.uint8, device="cpu"
        )

        # A list of buffers that will hold the gathered tensors.
        # Each buffer is a view into the pre‑allocated byte buffer.
        self._gather_buffers: List[torch.Tensor] = []

    def _ensure_buffers(self, tensor: torch.Tensor) -> None:
        """
        Ensure that the gather buffers are large enough to hold the incoming
        tensor. If the tensor is larger than the pre‑allocated buffer, the
        buffer is resized.
        """
        size = tensor.numel() * tensor.element_size()
        if size > self.max_buffer_size:
            # Resize the buffer to accommodate the new size
            self.max_buffer_size = size
            self._buffer = torch.empty(
                (self.max_buffer_size,), dtype=torch.uint8, device="cpu"
            )
        # Create a view of the buffer that matches the tensor shape
        self._gather_buffers = [
            torch.empty_like(tensor, device="cpu") for _ in range(self.num_ranks)
        ]

    def allgather(self, tensor: torch.Tensor) -> List[torch.Tensor]:
        """
        Perform an all‑gather operation on the provided tensor.

        Parameters
        ----------
        tensor : torch.Tensor
            The tensor to gather from all ranks.

        Returns
        -------
        List[torch.Tensor]
            A list of tensors, one from each rank.
        """
        if not dist.is_initialized():
            raise RuntimeError("torch.distributed is not initialized")

        # Ensure the gather buffers are ready
        self._ensure_buffers(tensor)

        # Move the tensor to CPU for gathering
        tensor_cpu = tensor.detach().cpu()

        # Perform the gather
        dist.all_gather(self._gather_buffers, tensor_cpu)

        # Return the gathered tensors as a list
        return self._gather_buffers


def create_fast_allgather_context(
    rank: int,
    node: int,
    num_ranks: int,
    num_nodes: int,
    max_buffer_size: int = 2 * 32 * 1024 * 1024,
) -> FastAllGatherContext:
    """
    Create a FastAllGatherContext for distributed communication.

    Parameters
    ----------
    rank : int
        Global rank of the current process.
    node : int
        Node identifier (used only for bookkeeping).
    num_ranks : int
        Total number of ranks in the world.
    num_nodes : int
        Total number of nodes in the world.
    max_buffer_size : int, optional
        Maximum size (in bytes) of the pre‑allocated gather buffer.

    Returns
    -------
    FastAllGatherContext
        A context object that can be used to perform efficient all‑gather
        operations.
    """
    # Initialize the process group if it hasn't been already.
    if not dist.is_available():
        raise RuntimeError("torch.distributed is not available")

    if not dist.is_initialized():
        # Default to gloo backend; users can override by setting
        # the environment variable TORCH_DISTRIBUTED_BACKEND.
        backend = dist.get_backend() if dist.is_available() else "gloo"
        dist.init_process_group(
            backend=backend,
            rank=rank,
            world_size=num_ranks,
        )

    return FastAllGatherContext(
        rank=rank,
        node=node,
        num_ranks=num_ranks,
        num_nodes=num_nodes,
        max_buffer_size=max_buffer_size,
    )