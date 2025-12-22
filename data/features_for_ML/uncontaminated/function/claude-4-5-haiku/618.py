def convert_layout_zero_stride(
    input: cute.Tensor | cute.Layout, ref_layout: cute.Layout
) -> cute.Layout:
    """
    Convert a layout by replacing zero strides with strides from a reference layout.
    
    This function takes an input layout (or extracts it from a tensor) and replaces
    any dimensions with zero stride with the corresponding stride from the reference layout.
    """
    # Extract layout from tensor if needed
    if isinstance(input, cute.Tensor):
        layout = input.layout()
    else:
        layout = input
    
    # Get the shape and strides from the layout
    shape = layout.shape()
    strides = layout.strides()
    
    # Get reference strides
    ref_strides = ref_layout.strides()
    
    # Replace zero strides with reference strides
    new_strides = []
    for i, stride in enumerate(strides):
        if stride == 0 and i < len(ref_strides):
            new_strides.append(ref_strides[i])
        else:
            new_strides.append(stride)
    
    # Create and return new layout with updated strides
    return cute.Layout(shape, new_strides)