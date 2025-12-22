import cute

def convert_layout_zero_stride(
    input: cute.Tensor | cute.Layout, ref_layout: cute.Layout
) -> cute.Layout:
    """
    Convert a layout or tensor to a new layout that matches the reference layout
    but sets the stride to zero for any dimension where the input has size 1
    (broadcastable dimension).

    Parameters
    ----------
    input : cute.Tensor | cute.Layout
        The input tensor or layout whose shape determines which dimensions
        should be broadcasted.
    ref_layout : cute.Layout
        The reference layout providing the base strides.

    Returns
    -------
    cute.Layout
        A new layout with the same shape as the input and strides from the
        reference layout, except that any dimension of size 1 in the input
        has a stride of zero.
    """
    # Determine the shape of the input
    if isinstance(input, cute.Layout):
        shape = input.shape
    else:
        shape = input.shape

    # Ensure the reference layout has the same rank
    if len(shape) != len(ref_layout.shape):
        raise ValueError(
            f"Input shape rank {len(shape)} does not match reference layout rank "
            f"{len(ref_layout.shape)}."
        )

    # Copy the reference strides and zero out broadcastable dimensions
    stride = list(ref_layout.stride)
    for i, dim in enumerate(shape):
        if dim == 1:
            stride[i] = 0

    # Construct and return the new layout
    return cute.Layout(shape, stride)