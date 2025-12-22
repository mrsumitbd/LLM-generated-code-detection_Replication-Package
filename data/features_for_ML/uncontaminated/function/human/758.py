import torch
import torch.distributed as dist

def scatter_fwd_all_gather_bwd(
    input: torch.Tensor,
    group: dist.ProcessGroup,
    dim: int,
    split_sizes: list[int] | None = None,
) -> torch.Tensor:
    return ScatterFwdAllGatherBwd.apply(input, group, dim, split_sizes)