def parse_wcs_capabilities(
    wcs, geoserver_url: str, search_term: Optional[str] = None
) -> List[GeoDataObject]:
    """Parses WCS GetCapabilities and returns a list of GeoDataObjects."""
    geo_data_objects = []
    
    try:
        contents = wcs.contents
    except Exception:
        return geo_data_objects
    
    for coverage_id in contents:
        try:
            coverage = contents[coverage_id]
            
            title = getattr(coverage, 'title', coverage_id)
            abstract = getattr(coverage, 'abstract', '')
            
            if search_term:
                search_lower = search_term.lower()
                if not (search_lower in title.lower() or search_lower in abstract.lower()):
                    continue
            
            bbox = None
            crs = None
            
            if hasattr(coverage, 'boundingboxes') and coverage.boundingboxes:
                bbox_info = coverage.boundingboxes[0]
                if isinstance(bbox_info, dict):
                    bbox = bbox_info.get('bbox')
                    crs = bbox_info.get('crs')
                else:
                    bbox = bbox_info
            
            if not bbox and hasattr(coverage, 'bbox'):
                bbox = coverage.bbox
            
            if not crs and hasattr(coverage, 'crsOptions') and coverage.crsOptions:
                crs = coverage.crsOptions[0]
            
            wcs_url = f"{geoserver_url}/ows?service=WCS&version=2.0.1&request=GetCoverage&coverageId={coverage_id}"
            
            geo_data_obj = GeoDataObject(
                name=coverage_id,
                title=title,
                abstract=abstract,
                data_type="WCS Coverage",
                url=wcs_url,
                bbox=bbox,
                crs=crs,
                source="WCS"
            )
            
            geo_data_objects.append(geo_data_obj)
            
        except Exception:
            continue
    
    return geo_data_objects