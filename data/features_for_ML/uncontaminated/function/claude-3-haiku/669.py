def init_dist_attn_runtime_key(
    q_ranges: AttnRanges,
    k_ranges: AttnRanges,
    attn_mask_type: list[AttnMaskType],
    total_seqlen_q: int,
    total_seqlen_k: int,
    pad_size: int,
    chunk_size: int,
    cp_group: dist.ProcessGroup,
    cp_mesh: DeviceMesh | None,
    dist_attn_config: DistAttnConfig,
) -> DistAttnRuntimeKey:
    # Compute the number of chunks for query and key sequences
    num_chunks_q = (total_seqlen_q + chunk_size - 1) // chunk_size
    num_chunks_k = (total_seqlen_k + chunk_size - 1) // chunk_size

    # Compute the start and end indices for each chunk
    q_chunk_start_end = [(i * chunk_size, min((i + 1) * chunk_size, total_seqlen_q)) for i in range(num_chunks_q)]
    k_chunk_start_end = [(i * chunk_size, min((i + 1) * chunk_size, total_seqlen_k)) for i in range(num_chunks_k)]

    # Compute the attention mask for each chunk
    attn_masks = []
    for mask_type in attn_mask_type:
        if mask_type == AttnMaskType.CAUSAL:
            attn_masks.append(torch.triu(torch.ones(chunk_size, chunk_size), diagonal=1).bool())
        elif mask_type == AttnMaskType.PADDING:
            attn_masks.append(torch.zeros(chunk_size, chunk_size).bool())
        else:
            raise ValueError(f"Unsupported attention mask type: {mask_type}")

    # Create the DistAttnRuntimeKey object
    runtime_key = DistAttnRuntimeKey(
        q_ranges=q_ranges,
        k_ranges=k_ranges,
        q_chunk_start_end=q_chunk_start_end,
        k_chunk_start_end=k_chunk_start_end,
        attn_masks=attn_masks,
        pad_size=pad_size,
        chunk_size=chunk_size,
        cp_group=cp_group,
        cp_mesh=cp_mesh,
        dist_attn_config=dist_attn_config,
    )

    return runtime_key