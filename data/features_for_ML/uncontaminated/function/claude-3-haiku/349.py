import requests
from typing import List, Optional
from lxml import etree
from .models import GeoDataObject

def parse_wcs_capabilities(
    wcs, geoserver_url: str, search_term: Optional[str] = None
) -> List[GeoDataObject]:
    """Parses WCS GetCapabilities and returns a list of GeoDataObjects."""
    capabilities_url = f"{geoserver_url}/wcs?service=WCS&request=GetCapabilities"
    response = requests.get(capabilities_url)
    root = etree.fromstring(response.content)

    data_objects = []
    for coverage in root.findall(".//wcs:CoverageDescription", namespaces=wcs.namespaces):
        identifier = coverage.find("wcs:Identifier", namespaces=wcs.namespaces).text
        if search_term and search_term.lower() not in identifier.lower():
            continue
        title = coverage.find("ows:Title", namespaces=wcs.namespaces).text
        abstract = coverage.find("ows:Abstract", namespaces=wcs.namespaces).text
        data_object = GeoDataObject(identifier, title, abstract)
        data_objects.append(data_object)

    return data_objects