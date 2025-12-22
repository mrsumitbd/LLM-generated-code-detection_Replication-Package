import cutlass.cute as cute
from cutlass import Float32, Int32, const_expr

def convert_layout_zero_stride(
    input: cute.Tensor | cute.Layout, ref_layout: cute.Layout
) -> cute.Layout:
    layout = input.layout if const_expr(isinstance(input, cute.Tensor)) else input
    # Group the modes with non-zero stride in the ref_layout together,
    # and the modes with zero stride together
    layout_flat = cute.flatten(layout)
    ref_layout_flat = cute.flatten(ref_layout)
    nonzero_modes = [i for i in range(cute.rank(layout_flat)) if ref_layout_flat[i].stride != 0]
    zero_modes = [i for i in range(cute.rank(layout_flat)) if ref_layout_flat[i].stride == 0]
    # There's an edge case when all modes are zero stride
    new_shape = (
        tuple(layout_flat[i].shape for i in nonzero_modes) if len(nonzero_modes) > 0 else (1,),
        tuple(layout_flat[i].shape for i in zero_modes),
    )
    new_stride = (
        tuple(layout_flat[i].stride for i in nonzero_modes) if len(nonzero_modes) > 0 else (0,),
        tuple(layout_flat[i].stride for i in zero_modes),
    )
    out_layout = cute.make_layout(new_shape, stride=new_stride)
    if const_expr(isinstance(input, cute.Tensor)):
        return cute.make_tensor(input.iterator, out_layout)
    else:
        return out_layout