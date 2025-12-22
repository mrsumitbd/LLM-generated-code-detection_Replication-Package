import random
from dataclasses import dataclass
from typing import List, Tuple

from PIL import Image

# Try to import the expected output type; fall back to a simple definition if unavailable.
try:
    from .infill_tile_output import InfillTileOutput  # type: ignore
except Exception:  # pragma: no cover
    @dataclass
    class InfillTileOutput:
        image: Image.Image
        tiles: List[Image.Image]


def _get_opaque_tiles(
    img: Image.Image, tile_size: int
) -> List[Tuple[int, int]]:
    """
    Return a list of top‑left coordinates of all fully opaque tiles of the given size.
    """
    w, h = img.size
    alpha = img.split()[-1]  # alpha channel
    alpha_data = alpha.load()

    tiles: List[Tuple[int, int]] = []

    for y in range(0, h - tile_size + 1, tile_size):
        for x in range(0, w - tile_size + 1, tile_size):
            fully_opaque = True
            for dy in range(tile_size):
                for dx in range(tile_size):
                    if alpha_data[x + dx, y + dy] == 0:
                        fully_opaque = False
                        break
                if not fully_opaque:
                    break
            if fully_opaque:
                tiles.append((x, y))
    return tiles


def infill_tile(
    image_to_infill: Image.Image, seed: int, tile_size: int
) -> InfillTileOutput:
    """Infills an image with random tiles from the image itself.

    If the image is not an RGBA image, it is returned untouched.

    Args:
        image_to_infill: The image to infill.
        seed: Random seed for reproducibility.
        tile_size: The size of the tiles to use for infilling.

    Raises:
        ValueError: If there are not enough opaque pixels to generate any tiles.
    """
    # Return unchanged if not RGBA
    if image_to_infill.mode != "RGBA":
        return InfillTileOutput(image=image_to_infill, tiles=[])

    # Find all fully opaque tiles in the source image
    opaque_tile_coords = _get_opaque_tiles(image_to_infill, tile_size)

    if not opaque_tile_coords:
        raise ValueError("Not enough opaque pixels to generate any tiles.")

    random.seed(seed)

    # Prepare output image
    out_img = Image.new("RGBA", image_to_infill.size)
    w, h = image_to_infill.size

    used_tiles: List[Image.Image] = []

    # Iterate over the grid of the output image
    for y in range(0, h, tile_size):
        for x in range(0, w, tile_size):
            # Choose a random source tile
            sx, sy = random.choice(opaque_tile_coords)
            tile = image_to_infill.crop((sx, sy, sx + tile_size, sy + tile_size))
            used_tiles.append(tile)

            # Paste onto output (handle partial tiles at edges)
            box = (x, y, x + tile_size, y + tile_size)
            out_img.paste(tile, box)

    return InfillTileOutput(image=out_img, tiles=used_tiles)