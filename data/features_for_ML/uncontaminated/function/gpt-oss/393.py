import os
from typing import Tuple, Union, Optional

try:
    import rasterio
except ImportError:
    rasterio = None


def get_current_raster_info(raster_layer: Optional[Union[str, rasterio.io.DatasetReader]] = None
                           ) -> Tuple[Tuple[float, float, float, float], int, int]:
    """
    Get current raster layer information for deriving pixel coordinates.

    Parameters
    ----------
    raster_layer : str or rasterio.io.DatasetReader, optional
        Path to a raster file or an already opened rasterio dataset.
        If None, the function will attempt to use the first raster file found
        in the current working directory.

    Returns
    -------
    tuple
        (extent, width, height)
        extent : tuple of (xmin, ymin, xmax, ymax)
        width : int, number of columns
        height : int, number of rows

    Raises
    ------
    FileNotFoundError
        If no raster file is found or the provided path does not exist.
    RuntimeError
        If rasterio is not installed or cannot open the raster.
    """
    # Helper to open a rasterio dataset
    def _open_dataset(path: str) -> rasterio.io.DatasetReader:
        if not rasterio:
            raise RuntimeError("rasterio is required to open raster files.")
        return rasterio.open(path)

    # Determine the dataset
    if raster_layer is None:
        # Search for a raster file in the current directory
        raster_extensions = ('.tif', '.tiff', '.img', '.jp2', '.vrt')
        for fname in os.listdir('.'):
            if fname.lower().endswith(raster_extensions):
                raster_layer = fname
                break
        if raster_layer is None:
            raise FileNotFoundError("No raster file found in the current directory.")
    if isinstance(raster_layer, str):
        if not os.path.isfile(raster_layer):
            raise FileNotFoundError(f"Raster file not found: {raster_layer}")
        dataset = _open_dataset(raster_layer)
    elif hasattr(raster_layer, 'bounds') and hasattr(raster_layer, 'width') and hasattr(raster_layer, 'height'):
        dataset = raster_layer
    else:
        raise TypeError("raster_layer must be a file path or a rasterio DatasetReader.")

    # Extract extent, width, height
    bounds = dataset.bounds
    extent = (bounds.left, bounds.bottom, bounds.right, bounds.top)
    width = dataset.width
    height = dataset.height

    # Close dataset if we opened it
    if isinstance(raster_layer, str):
        dataset.close()

    return extent, width, height