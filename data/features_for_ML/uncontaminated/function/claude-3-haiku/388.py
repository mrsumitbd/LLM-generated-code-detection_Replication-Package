import torch
import torch.distributed as dist

def native_group_cast_impl(
    input: torch.Tensor,
    output: torch.Tensor | None,
    input_split_sizes: list[int] | torch.Tensor,
    output_split_sizes: list[int] | torch.Tensor,
    dst_indices: list[list[int]] | torch.Tensor,
    src_index: list[int] | torch.Tensor,
    group: dist.ProcessGroup,
    async_op: bool = False,
    cast_lse: bool = False,
    input_lse: torch.Tensor | None = None,
    output_lse: torch.Tensor | None = None,
    **kwargs,
) -> WorkWithPostProcessFn:
    """Native group-cast implementation"""
    work = dist.all_to_all_single(
        output,
        input,
        output_split_sizes,
        input_split_sizes,
        dst_indices,
        src_index,
        group,
        async_op=async_op,
    )

    if cast_lse:
        if input_lse is None or output_lse is None:
            raise ValueError("input_lse and output_lse must be provided when cast_lse is True")
        work.wait()
        torch.linalg.lstsq(output, input_lse, output_lse, driver="gels")

    return work