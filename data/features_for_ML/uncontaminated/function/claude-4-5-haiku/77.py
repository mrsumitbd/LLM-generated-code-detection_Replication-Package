from pathlib import Path
from typing import Literal
import anthropic


def _classify(path: Path) -> Literal["raster", "vector", "other"]:
    """
    Classify a file as raster, vector, or other based on its path/extension.
    Uses Claude to make the classification decision.
    """
    client = anthropic.Anthropic()
    
    filename = path.name
    suffix = path.suffix.lower()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": f"""Classify the following file as either "raster", "vector", or "other" based on its filename and extension.

File: {filename}
Extension: {suffix}

Raster files are image formats like: .tif, .tiff, .jp2, .png, .jpg, .jpeg, .gif, .bmp, .img, .hdf, .nc, .grd, .asc, .dem, .sid, .ecw
Vector files are geographic data formats like: .shp, .geojson, .json, .gpkg, .gdb, .kml, .kmz, .gml, .gpx, .dgn, .dwg, .dxf
Other files are anything else.

Respond with ONLY one word: "raster", "vector", or "other"."""
            }
        ]
    )
    
    response = message.content[0].text.strip().lower()
    
    if response in ["raster", "vector", "other"]:
        return response
    
    return "other"