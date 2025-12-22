def get_current_raster_info(raster_layer=None):
    if raster_layer is None:
        return None
    
    extent = raster_layer.extent()
    width = raster_layer.width()
    height = raster_layer.height()
    
    return extent, width, height