from rembg import remove
from PIL import Image

def remove_background(image: Image.Image,
                      rembg_session: Any = None,
                      force: bool = False,
                      **rembg_kwargs):
    if rembg_session is None or force:
        result = remove(image.tobytes(), **rembg_kwargs)
        return Image.frombytes(image.mode, image.size, result)
    else:
        return rembg_session.remove(image)