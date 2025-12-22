import cutlass.torch as cutlass_torch
from cutlass.cute.runtime import from_dlpack, make_ptr
import cutlass
import torch

def create_and_permute_tensor(l, mode0, mode1, is_mode0_major, dtype, is_dynamic_layout=True):
        # is_mode0_major: (l, mode1, mode0) -> (mode0, mode1, l)
        # else: (l, mode0, mode1) -> (mode0, mode1, l)
        shape = (l, mode1, mode0) if is_mode0_major else (l, mode0, mode1)
        permute_order = (2, 1, 0) if is_mode0_major else (1, 2, 0)
        is_unsigned = dtype in {cutlass.Uint8}
        # Temporarily use uint8 as torch does not support fp8 type
        torch_dtype = cutlass_torch.dtype(dtype)
        gen_dtype = (
            torch_dtype
            if dtype not in {cutlass.Float8E5M2, cutlass.Float8E4M3FN}
            else torch.bfloat16
        )

        # Create dtype torch tensor (cpu)
        torch_tensor_cpu = cutlass_torch.create_and_permute_torch_tensor(
            shape,
            gen_dtype,
            permute_order=permute_order,
            # init_type=cutlass.torch.TensorInitType.RANDOM,
            # init_config=cutlass.torch.RandomInitConfig(
            #     min_val=0 if is_unsigned else -2, max_val=4 if is_unsigned else 2
            # ),
            init_type=cutlass.torch.TensorInitType.GAUSSIAN,
            init_config=cutlass.torch.GaussianInitConfig(std=k ** (-0.5), scale=1),
        ).to(torch_dtype)
        # Create dtype torch tensor (gpu)
        torch_tensor = torch_tensor_cpu.cuda()

        # Create f32 torch tensor (cpu)
        f32_torch_tensor = torch_tensor_cpu.to(dtype=torch.float32)

        # Create dtype cute tensor (gpu)
        torch_tensor_view = (
            torch_tensor
            if dtype not in {cutlass.Float8E5M2, cutlass.Float8E4M3FN}
            else torch_tensor.view(torch.uint8)
        )
        cute_tensor = from_dlpack(torch_tensor_view, assumed_align=16)
        cute_tensor.element_type = dtype
        if is_dynamic_layout:
            cute_tensor = cute_tensor.mark_layout_dynamic(leading_dim=(0 if is_mode0_major else 1))
        cute_tensor = cutlass_torch.convert_cute_tensor(
            f32_torch_tensor,
            cute_tensor,
            dtype,
            is_dynamic_layout=is_dynamic_layout,
        )

        return f32_torch_tensor, cute_tensor, torch_tensor, torch_tensor_cpu