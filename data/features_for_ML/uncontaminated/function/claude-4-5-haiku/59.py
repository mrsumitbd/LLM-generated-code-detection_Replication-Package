def replace_ls(old_ls: TIMMLayerScale):
    """Replace a TIMMLayerScale layer with an equivalent LayerScale layer."""
    if old_ls is None:
        return None
    
    # Create a new LayerScale with the same configuration
    new_ls = LayerScale(
        dim=old_ls.dim,
        init_values=old_ls.init_values,
        inplace=old_ls.inplace
    )
    
    # Copy the learned scale parameters
    if hasattr(old_ls, 'gamma'):
        new_ls.gamma.data.copy_(old_ls.gamma.data)
    
    return new_ls