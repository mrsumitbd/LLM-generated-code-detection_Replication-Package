def convert_layout_zero_stride(input, ref_layout):
    if isinstance(input, cute.Tensor):
        input = input.layout
    new_layout = cute.Layout()
    for dim in ref_layout:
        if dim in input:
            new_layout[dim] = input[dim]
        else:
            new_layout[dim] = 0
    return new_layout