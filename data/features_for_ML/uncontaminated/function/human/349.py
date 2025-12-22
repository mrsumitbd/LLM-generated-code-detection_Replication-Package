from urllib.parse import urlencode, urljoin
from models.geodata import DataOrigin, DataType, GeoDataObject
from typing import Any, Dict, List, Optional, Tuple, Union

def parse_wcs_capabilities(
    wcs, geoserver_url: str, search_term: Optional[str] = None
) -> List[GeoDataObject]:
    """Parses WCS GetCapabilities and returns a list of GeoDataObjects."""
    layers: List[GeoDataObject] = []
    base_url = geoserver_url.split("?")[0]

    for cov_id, cov in wcs.contents.items():
        title = cov.title or cov.id
        abstract = cov.abstract or ""
        if search_term and not (
            search_term.lower() in title.lower()
            or search_term.lower() in abstract.lower()
            or search_term.lower() in cov_id.lower()
        ):
            continue

        bounding_box = None
        if cov.boundingBoxWGS84:
            min_lon, min_lat, max_lon, max_lat = cov.boundingBoxWGS84
            bounding_box = (
                f"POLYGON(({max_lon} {min_lat}, {max_lon} {max_lat}, "
                f"{min_lon} {max_lat}, {min_lon} {min_lat}, {max_lon} {min_lat}))"
            )

        params = {
            "service": "WCS",
            "version": "2.0.1",
            "request": "GetCoverage",
            "coverageId": cov.id,
        }
        data_link = f"{base_url}?{urlencode(params)}"

        geo_object = GeoDataObject(
            id=f"wcs_{cov.id}",
            data_source_id=f"geoserver_{cov.id}",
            data_type=DataType.RASTER,
            data_origin=DataOrigin.TOOL.value,
            data_source=wcs.provider.name or "Unknown",
            data_link=data_link,
            name=cov.id,
            title=title,
            description=abstract,
            bounding_box=bounding_box,
            layer_type="WCS",
            properties=_sanitize_properties(
                {"supported_formats": getattr(cov, "supportedFormats", [])}
            ),
        )
        layers.append(geo_object)
    return layers