from typing import Any
import io
from PIL import Image
import rembg

def remove_background(
    image: Image.Image,
    rembg_session: Any = None,
    force: bool = False,
    **rembg_kwargs,
) -> Image.Image:
    """
    Remove the background from a PIL image using the rembg library.

    Parameters
    ----------
    image : PIL.Image.Image
        The input image.
    rembg_session : Any, optional
        A pre‑created rembg session. If None, a new session will be created.
    force : bool, default False
        If True, the background will be removed even if the image already has an alpha channel.
    **rembg_kwargs
        Additional keyword arguments passed to rembg.remove.

    Returns
    -------
    PIL.Image.Image
        The image with the background removed (RGBA).
    """
    # If the image already has an alpha channel and we are not forcing, return it unchanged
    if not force and image.mode == "RGBA":
        return image

    # Ensure we have a session
    session = rembg_session or rembg.new_session()

    # Convert the image to bytes
    with io.BytesIO() as buf:
        image.save(buf, format="PNG")
        buf.seek(0)
        input_bytes = buf.read()

    # Remove background
    output_bytes = rembg.remove(input_bytes, session=session, **rembg_kwargs)

    # Load the result into a PIL image
    with io.BytesIO(output_bytes) as out_buf:
        out_buf.seek(0)
        result = Image.open(out_buf).convert("RGBA")

    return result