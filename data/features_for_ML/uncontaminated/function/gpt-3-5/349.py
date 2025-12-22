def parse_wcs_capabilities(wcs, geoserver_url: str, search_term: Optional[str] = None) -> List[GeoDataObject]:
    capabilities_url = f"{geoserver_url}/wcs?request=GetCapabilities"
    response = requests.get(capabilities_url)
    if response.status_code == 200:
        capabilities_xml = response.text
        capabilities = xmltodict.parse(capabilities_xml)
        geo_data_objects = []
        for coverage in capabilities['Capabilities']['Contents']['CoverageSummary']:
            if search_term is None or search_term.lower() in coverage['Title'].lower():
                geo_data_object = GeoDataObject(
                    title=coverage['Title'],
                    abstract=coverage.get('Abstract', ''),
                    keywords=coverage.get('Keywords', ''),
                    crs=coverage.get('SupportedCRS', ''),
                    bbox=coverage.get('WGS84BoundingBox', ''),
                    formats=coverage.get('SupportedFormat', '')
                )
                geo_data_objects.append(geo_data_object)
        return geo_data_objects
    else:
        return []