from __future__ import annotations

try:
    # Try to import the existing GrpCollConfig if it is defined elsewhere
    from .config import GrpCollConfig  # type: ignore
except Exception:
    # Fallback definition if not available
    from dataclasses import dataclass

    @dataclass
    class GrpCollConfig:
        """Fallback configuration for group collectives."""
        group_size: int
        num_groups: int


def get_default_group_cast_config(num_ranks: int) -> "GrpCollConfig":
    """
    Get a recommended dispatch config.

    Argument:
        num_ranks: the number of ranks.

    Returns:
        config: the recommended config.
    """
    if num_ranks <= 0:
        raise ValueError("num_ranks must be a positive integer")

    # Heuristic: choose a group size that is a power of two and scales with the number of ranks.
    if num_ranks <= 8:
        group_size = 2
    elif num_ranks <= 32:
        group_size = 4
    elif num_ranks <= 128:
        group_size = 8
    elif num_ranks <= 512:
        group_size = 16
    else:
        group_size = 32

    # Ensure group_size does not exceed num_ranks
    group_size = min(group_size, num_ranks)

    # Compute the number of groups needed to cover all ranks
    num_groups = (num_ranks + group_size - 1) // group_size

    return GrpCollConfig(group_size=group_size, num_groups=num_groups)