def get_current_raster_info(raster_layer=None):
    """Get current raster layer information for deriving pixel coordinates.
    Returns:
        tuple: extent, width, height of the raster layer
    """
    if raster_layer is None:
        from qgis.core import QgsProject
        layers = QgsProject.instance().mapLayers().values()
        raster_layer = None
        for layer in layers:
            if layer.type() == 1:  # QgsMapLayer.RasterLayer
                raster_layer = layer
                break
        if raster_layer is None:
            return None, None, None
    
    extent = raster_layer.extent()
    width = raster_layer.width()
    height = raster_layer.height()
    
    return extent, width, height