def build_query_params(options: Optional[QueryOptions] = None) -> dict:
    """Build OData query parameters dict from options

    Args:
        options: Query options to convert

    Returns:
        Dictionary of query parameters
    """
    if options is None:
        return {}
    
    params = {}
    
    if hasattr(options, 'select') and options.select:
        params['$select'] = ','.join(options.select) if isinstance(options.select, list) else options.select
    
    if hasattr(options, 'filter') and options.filter:
        params['$filter'] = options.filter
    
    if hasattr(options, 'orderby') and options.orderby:
        params['$orderby'] = options.orderby
    
    if hasattr(options, 'top') and options.top is not None:
        params['$top'] = options.top
    
    if hasattr(options, 'skip') and options.skip is not None:
        params['$skip'] = options.skip
    
    if hasattr(options, 'expand') and options.expand:
        params['$expand'] = ','.join(options.expand) if isinstance(options.expand, list) else options.expand
    
    if hasattr(options, 'count') and options.count:
        params['$count'] = 'true'
    
    if hasattr(options, 'search') and options.search:
        params['$search'] = options.search
    
    return params