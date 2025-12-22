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
        return InfillTileOutput(image=image_to_infill)
    
    random.seed(seed)
    np.random.seed(seed)
    
    image_array = np.array(image_to_infill)
    alpha_channel = image_array[:, :, 3]
    
    # Find all opaque pixels (alpha > 128)
    opaque_mask = alpha_channel > 128
    opaque_coords = np.argwhere(opaque_mask)
    
    if len(opaque_coords) == 0:
        raise ValueError("There are not enough opaque pixels to generate any tiles.")
    
    # Create a copy of the image to infill
    infilled_array = image_array.copy()
    
    # Find all transparent pixels (alpha <= 128)
    transparent_mask = alpha_channel <= 128
    transparent_coords = np.argwhere(transparent_mask)
    
    if len(transparent_coords) == 0:
        return InfillTileOutput(image=image_to_infill)
    
    # For each transparent pixel, find a random opaque tile and copy it
    for trans_y, trans_x in transparent_coords:
        # Randomly select an opaque pixel
        rand_idx = random.randint(0, len(opaque_coords) - 1)
        opaque_y, opaque_x = opaque_coords[rand_idx]
        
        # Calculate tile boundaries for the opaque pixel
        tile_start_y = max(0, opaque_y - tile_size // 2)
        tile_end_y = min(image_array.shape[0], tile_start_y + tile_size)
        tile_start_x = max(0, opaque_x - tile_size // 2)
        tile_end_x = min(image_array.shape[1], tile_start_x + tile_size)
        
        # Adjust if tile goes out of bounds
        if tile_end_y - tile_start_y < tile_size:
            tile_start_y = max(0, tile_end_y - tile_size)
        if tile_end_x - tile_start_x < tile_size:
            tile_start_x = max(0, tile_end_x - tile_size)
        
        # Get the tile
        tile = image_array[tile_start_y:tile_end_y, tile_start_x:tile_end_x]
        
        # Calculate offset within tile
        offset_y = opaque_y - tile_start_y
        offset_x = opaque_x - tile_start_x
        
        # Calculate source position in tile relative to transparent pixel
        src_y = offset_y
        src_x = offset_x
        
        if 0 <= src_y < tile.shape[0] and 0 <= src_x < tile.shape[1]:
            infilled_array[trans_y, trans_x] = tile[src_y, src_x]
    
    infilled_image = Image.fromarray(infilled_array, mode="RGBA")
    return InfillTileOutput(image=infilled_image)