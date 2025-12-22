from timm.layers import TIMMLayerScale

def replace_ls(old_ls: TIMMLayerScale):
    """
    Replace a TIMMLayerScale instance with a new one that has the same underlying
    layer but resets the scaling factor to 1.0 and the bias to 0.0.

    Parameters
    ----------
    old_ls : TIMMLayerScale
        The original TIMMLayerScale instance to be replaced.

    Returns
    -------
    TIMMLayerScale
        A new TIMMLayerScale instance with the same layer but with a neutral
        scaling factor and bias.
    """
    # Preserve the original layer
    layer = old_ls.layer

    # Create a new TIMMLayerScale with neutral scaling and bias
    new_ls = TIMMLayerScale(layer, scale=1.0, bias=0.0)

    return new_ls