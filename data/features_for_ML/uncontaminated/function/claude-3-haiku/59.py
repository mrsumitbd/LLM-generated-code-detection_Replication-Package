def replace_ls(old_ls: TIMMLayerScale):
    new_ls = TIMMLayerScale(
        in_channels=old_ls.in_channels,
        out_channels=old_ls.out_channels,
        kernel_size=old_ls.kernel_size,
        stride=old_ls.stride,
        padding=old_ls.padding,
        dilation=old_ls.dilation,
        groups=old_ls.groups,
        bias=old_ls.bias,
        padding_mode=old_ls.padding_mode,
        device=old_ls.device,
        dtype=old_ls.dtype
    )
    return new_ls