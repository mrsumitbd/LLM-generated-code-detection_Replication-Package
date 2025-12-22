from PIL import Image
import random
from collections import namedtuple

InfillTileOutput = namedtuple('InfillTileOutput', ['image', 'tiles'])

def infill_tile(image_to_infill: Image.Image, seed: int, tile_size: int) -> InfillTileOutput:
    if image_to_infill.mode != 'RGBA':
        return InfillTileOutput(image_to_infill, [])

    random.seed(seed)
    width, height = image_to_infill.size
    tiles = []

    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            tile = image_to_infill.crop((x, y, x + tile_size, y + tile_size))
            if tile.getextrema()[3][0] > 0:
                tiles.append(tile)

    if not tiles:
        raise ValueError("Not enough opaque pixels to generate any tiles.")

    return InfillTileOutput(image_to_infill, tiles)