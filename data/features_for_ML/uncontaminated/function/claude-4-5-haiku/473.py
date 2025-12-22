def remove_background(image: PIL.Image.Image,
    rembg_session: Any = None,
    force: bool = False,
    **rembg_kwargs,
) -> PIL.Image.Image:
    try:
        import rembg
    except ImportError:
        if force:
            raise ImportError("rembg is not installed. Please install it to use background removal.")
        return image
    
    if rembg_session is None:
        rembg_session = rembg.new_session()
    
    output = rembg.remove(image, session=rembg_session, **rembg_kwargs)
    
    return output