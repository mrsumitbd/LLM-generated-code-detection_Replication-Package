def get_current_raster_info(raster_layer=None):
        """Get current raster layer information for deriving pixel coordinates.
        Returns:
            tuple: extent, width, height of the raster layer
        """

        if not raster_layer:
            raise ValueError("No raster layer found")

        # Get raster dimensions and extent
        extent = raster_layer.extent()
        width = raster_layer.width()
        height = raster_layer.height()
        crs = raster_layer.crs()

        return extent, width, height, crs