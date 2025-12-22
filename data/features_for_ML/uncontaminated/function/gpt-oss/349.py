from typing import List, Optional

def parse_wcs_capabilities(
    wcs, geoserver_url: str, search_term: Optional[str] = None
) -> List["GeoDataObject"]:
    """Parses WCS GetCapabilities and returns a list of GeoDataObjects."""
    # Import lxml for XML parsing
    try:
        from lxml import etree as ET
    except Exception as exc:  # pragma: no cover - defensive
        raise ImportError("lxml is required for parsing WCS capabilities") from exc

    # Attempt to import GeoDataObject from geoserver-client. If unavailable, create a minimal dataclass.
    try:
        from geoserver.catalog import GeoDataObject  # type: ignore
    except Exception:  # pragma: no cover - fallback
        from dataclasses import dataclass

        @dataclass
        class GeoDataObject:  # type: ignore
            name: str
            title: str
            abstract: Optional[str] = None
            bbox: Optional[tuple] = None
            crs: Optional[str] = None

    # Retrieve the capabilities XML. The wcs object may return a string or an Element.
    capabilities = wcs.get_capabilities()
    if isinstance(capabilities, str):
        root = ET.fromstring(capabilities.encode("utf-8"))
    else:
        root = capabilities

    # Namespace mapping for WCS 2.0.1
    ns = {"wcs": "http://www.opengis.net/wcs/2.0"}

    # Find all CoverageSummary elements
    coverage_summaries = root.xpath("//wcs:CoverageSummary", namespaces=ns)
    results: List[GeoDataObject] = []
    for cs in coverage_summaries:
        # Extract name, title, abstract
        name_el = cs.find("wcs:CoverageId", namespaces=ns)
        title_el = cs.find("wcs:Title", namespaces=ns)
        abstract_el = cs.find("wcs:Abstract", namespaces=ns)
        if name_el is None or title_el is None:
            continue
        name = name_el.text or ""
        title = title_el.text or ""
        abstract = abstract_el.text if abstract_el is not None else None

        # Filter by search_term if provided
        if search_term:
            term = search_term.lower()
            if term not in name.lower() and term not in title.lower():
                continue

        # Extract bounding box (take the first one if multiple)
        bbox_el = cs.find("wcs:BoundingBox", namespaces=ns)
        bbox = None
        crs = None
        if bbox_el is not None:
            crs = bbox_el.get("crs")
            lower = bbox_el.find("wcs:LowerCorner", namespaces=ns)
            upper = bbox_el.find("wcs:UpperCorner", namespaces=ns)
            if lower is not None and upper is not None:
                try:
                    lower_coords = [float(v) for v in lower.text.split()]
                    upper_coords = [float(v) for v in upper.text.split()]
                    if len(lower_coords) == len(upper_coords):
                        bbox = tuple(lower_coords + upper_coords)
                except Exception:  # pragma: no cover - malformed coordinates
                    bbox = None

        obj = GeoDataObject(name=name, title=title, abstract=abstract, bbox=bbox, crs=crs)
        results.append(obj)

    return results