def convert_layout_zero_stride(
    input: cute.Tensor | cute.Layout, ref_layout: cute.Layout
) -> cute.Layout:
    if isinstance(input, cute.Tensor):
        input_layout = input.layout
    else:
        input_layout = input

    new_layout = cute.Layout(
        input_layout.sizes,
        input_layout.strides,
        input_layout.device,
        input_layout.dtype,
    )

    for i in range(len(new_layout.strides)):
        if new_layout.strides[i] == 0:
            new_layout.strides[i] = ref_layout.strides[i]

    return new_layout