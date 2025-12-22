from PIL import Image
import numpy as np

def infill_tile(image_to_infill: Image.Image, seed: int, tile_size: int) -> InfillTileOutput:
    """Infills an image with random tiles from the image itself.

    If the image is not an RGBA image, it is returned untouched.

    Args:
        image: The image to infill.
        tile_size: The size of the tiles to use for infilling.

    Raises:
        ValueError: If there are not enough opaque pixels to generate any tiles.
    """

    if image_to_infill.mode != "RGBA":
        return InfillTileOutput(infilled=image_to_infill)

    # Internally, we want a tuple of (tile_width, tile_height). In the future, the tile size can be any rectangle.
    _tile_size = (tile_size, tile_size)
    np_image = np.array(image_to_infill, dtype=np.uint8)

    # Create the pool of tiles that we will use to infill
    tile_pool = create_tile_pool(np_image, _tile_size)

    # Create an image from the tiles, same size as the original
    tile_np_image = create_filled_image(np_image, tile_pool, _tile_size, seed)

    # Paste the OG image over the tile image, effectively infilling the area
    tile_image = Image.fromarray(tile_np_image, "RGB")
    infilled = tile_image.copy()
    infilled.paste(image_to_infill, (0, 0), image_to_infill.split()[-1])

    # I think we want this to be "RGBA"?
    infilled.convert("RGBA")

    return InfillTileOutput(infilled=infilled, tile_image=tile_image)