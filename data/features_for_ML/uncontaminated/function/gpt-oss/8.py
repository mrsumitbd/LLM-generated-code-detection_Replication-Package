import torch

def create_and_permute_tensor(l, mode0, mode1, is_mode0_major, dtype, is_dynamic_layout=True):
    """
    Create a 3‑D tensor with shape determined by `is_mode0_major` and then
    permute it to the order (mode0, mode1, l).

    Parameters
    ----------
    l : int
        Size of the first dimension in the original layout.
    mode0 : int
        Size of the second dimension in the original layout when
        `is_mode0_major` is False, otherwise the third dimension.
    mode1 : int
        Size of the third dimension in the original layout when
        `is_mode0_major` is False, otherwise the second dimension.
    is_mode0_major : bool
        If True, the original layout is (l, mode1, mode0) and the
        permutation is (2, 1, 0).  If False, the original layout is
        (l, mode0, mode1) and the permutation is (1, 2, 0).
    dtype : torch.dtype or str
        Data type of the tensor.  If a string is provided, it is
        converted to a torch dtype.
    is_dynamic_layout : bool, optional
        If True, the tensor is created with a dynamic layout
        (default).  If False, a static layout is used.  In practice
        this flag is ignored because PyTorch does not expose
        static/dynamic layout differences directly; the flag is
        kept for API compatibility.

    Returns
    -------
    torch.Tensor
        The permuted tensor of shape (mode0, mode1, l).
    """
    # Resolve dtype if a string is passed
    if isinstance(dtype, str):
        dtype = getattr(torch, dtype)

    # Determine the original shape and permutation
    if is_mode0_major:
        orig_shape = (l, mode1, mode0)
        perm = (2, 1, 0)
    else:
        orig_shape = (l, mode0, mode1)
        perm = (1, 2, 0)

    # Create the tensor.  The `is_dynamic_layout` flag is not
    # directly supported by PyTorch, so we simply create a normal
    # tensor.  If a different layout is required, the caller can
    # adjust the tensor after creation.
    tensor = torch.empty(orig_shape, dtype=dtype)

    # Permute to the desired order
    return tensor.permute(perm)