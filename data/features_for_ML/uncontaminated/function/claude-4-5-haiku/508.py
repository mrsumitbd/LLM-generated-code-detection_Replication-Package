def ifftn(
    a: Union[Quantity, jax.typing.ArrayLike],
    s: Shape | None = None,
    axes: Sequence[int] | None = None,
    norm: str | None = None
) -> Union[Quantity, jax.typing.ArrayLike]:
    if isinstance(a, Quantity):
        # For Quantity objects, we need to handle the unit transformation
        # ifftn reduces dimensions, so we divide by the product of the transform sizes
        value = a.value
        unit = a.unit
        
        # Determine the axes and shape for the transform
        if axes is None:
            if s is None:
                axes = tuple(range(value.ndim))
                transform_shape = value.shape
            else:
                axes = tuple(range(len(s)))
                transform_shape = s
        else:
            axes = tuple(axes)
            if s is None:
                transform_shape = tuple(value.shape[ax] for ax in axes)
            else:
                transform_shape = tuple(s)
        
        # Compute the product of transform dimensions
        size_product = 1
        for dim_size in transform_shape:
            size_product *= dim_size
        
        # Apply ifftn to the value
        result_value = jnp.fft.ifftn(value, s=s, axes=axes, norm=norm)
        
        # The unit is divided by the product of the transform sizes
        # (inverse FFT scales by 1/N where N is the product of dimensions)
        result_unit = unit / size_product
        
        return Quantity(result_value, result_unit)
    else:
        # For non-Quantity arrays, just apply ifftn directly
        return jnp.fft.ifftn(a, s=s, axes=axes, norm=norm)