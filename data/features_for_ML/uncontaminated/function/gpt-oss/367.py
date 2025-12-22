import numpy as np

def masked_min(*args, **kwargs):
    """
    Compute the minimum of an array while ignoring masked values.

    Parameters
    ----------
    a : array_like
        Input array.
    mask : array_like, optional
        Boolean mask array of the same shape as `a`. True values are masked.
    axis : int or tuple of ints, optional
        Axis or axes along which to compute the minimum.
    out : ndarray, optional
        Alternative output array in which to place the result.
    keepdims : bool, optional
        If True, the reduced axes are left in the result as dimensions with size one.

    Returns
    -------
    min : scalar or ndarray
        The minimum value(s) of the input array, ignoring masked elements.
    """
    if not args:
        raise TypeError("masked_min() missing required positional argument: 'a'")

    a = args[0]
    mask = None

    # Determine mask from positional or keyword arguments
    if len(args) > 1:
        mask = args[1]
    else:
        mask = kwargs.pop('mask', None)

    # If the input is already a masked array and no explicit mask is given,
    # use it directly; otherwise create a new masked array.
    if isinstance(a, np.ma.MaskedArray) and mask is None:
        ma = a
    else:
        ma = np.ma.array(a, mask=mask)

    # Forward remaining keyword arguments to the masked array's min method.
    return ma.min(**kwargs)