def get_current_raster_info(raster_layer=None):
    """Get current raster layer information for deriving pixel coordinates.
    Returns:
        tuple: extent, width, height of the raster layer
    """
    if raster_layer is None:
        raster_layer = arcpy.GetRasterProperties_management("", "CURRENT")

    extent = raster_layer.extent
    width = raster_layer.width
    height = raster_layer.height

    return (extent, width, height)