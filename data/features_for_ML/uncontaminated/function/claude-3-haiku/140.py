from typing import Tuple
from PIL import Image
import random

InfillTileOutput = Tuple[Image.Image, int]

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
        return image_to_infill, 0

    random.seed(seed)
    width, height = image_to_infill.size
    tiles = []

    for x in range(0, width, tile_size):
        for y in range(0, height, tile_size):
            tile = image_to_infill.crop((x, y, x + tile_size, y + tile_size))
            if any(pixel[3] > 0 for pixel in tile.getdata()):
                tiles.append(tile)

    if not tiles:
        raise ValueError("Not enough opaque pixels to generate any tiles.")

    infilled_image = Image.new("RGBA", image_to_infill.size)
    num_tiles_placed = 0

    while True:
        x = random.randint(0, width - tile_size)
        y = random.randint(0, height - tile_size)
        tile = random.choice(tiles)
        if all(infilled_image.getpixel((x + px, y + py))[3] == 0 for px in range(tile_size) for py in range(tile_size)):
            infilled_image.paste(tile, (x, y))
            num_tiles_placed += 1
        if num_tiles_placed >= len(tiles):
            break

    return infilled_image, num_tiles_placed