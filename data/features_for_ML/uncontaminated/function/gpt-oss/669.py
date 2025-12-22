from __future__ import annotations

from typing import List

import torch.distributed as dist
from torch.distributed.device_mesh import DeviceMesh

# Assume these types are defined elsewhere in the codebase.
# If they are not available, the imports below will fail, but the
# implementation logic remains the same.
try:
    from .types import AttnRanges, AttnMaskType, DistAttnConfig, DistAttnRuntimeKey
except Exception:
    # Fallback definitions for type checking / documentation purposes.
    from dataclasses import dataclass

    @dataclass
    class AttnRanges:
        start: int
        end: int

    class AttnMaskType:
        pass

    @dataclass
    class DistAttnConfig:
        pass

    @dataclass
    class DistAttnRuntimeKey:
        q_ranges: AttnRanges
        k_ranges: AttnRanges
        attn_mask_type: tuple[AttnMaskType, ...]
        total_seqlen_q: int
        total_seqlen_k: int
        pad_size: int
        chunk_size: int
        cp_group: dist.ProcessGroup
        cp_mesh: DeviceMesh | None
        dist_attn_config: DistAttnConfig


def init_dist_attn_runtime_key(
    q_ranges: AttnRanges,
    k_ranges: AttnRanges,
    attn_mask_type: List[AttnMaskType],
    total_seqlen_q: int,
    total_seqlen_k: int,
    pad_size: int,
    chunk_size: int,
    cp_group: dist.ProcessGroup,
    cp_mesh: DeviceMesh | None,
    dist_attn_config: DistAttnConfig,
) -> DistAttnRuntimeKey:
    """
    Construct a DistAttnRuntimeKey that uniquely identifies a distributed
    attention configuration for caching or lookup purposes.

    Parameters
    ----------
    q_ranges : AttnRanges
        The query range for the current process.
    k_ranges : AttnRanges
        The key range for the current process.
    attn_mask_type : list[AttnMaskType]
        The list of attention mask types applied.
    total_seqlen_q : int
        Total sequence length for queries across all processes.
    total_seqlen_k : int
        Total sequence length for keys across all processes.
    pad_size : int
        Padding size applied to the sequences.
    chunk_size : int
        Size of the chunk used for processing.
    cp_group : dist.ProcessGroup
        The process group used for communication.
    cp_mesh : DeviceMesh | None
        The device mesh used for communication, if any.
    dist_attn_config : DistAttnConfig
        Configuration object for distributed attention.

    Returns
    -------
    DistAttnRuntimeKey
        A key object that can be used to cache or identify the runtime
        configuration.
    """
    # Convert the list of mask types to a tuple to make the key hashable.
    mask_tuple = tuple(attn_mask_type)

    # Construct and return the runtime key.
    return DistAttnRuntimeKey(
        q_ranges=q_ranges,
        k_ranges=k_ranges,
        attn_mask_type=mask_tuple,
        total_seqlen_q=total_seqlen_q,
        total_seqlen_k=total_seqlen_k,
        pad_size=pad_size,
        chunk_size=chunk_size,
        cp_group=cp_group,
        cp_mesh=cp_mesh,
        dist_attn_config=dist_attn_config,
    )