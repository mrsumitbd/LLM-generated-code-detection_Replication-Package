def build_query_params(options: Optional[QueryOptions] = None) -> dict:
    query_params = {}
    if options:
        if options.filter:
            query_params['$filter'] = options.filter
        if options.select:
            query_params['$select'] = options.select
        if options.expand:
            query_params['$expand'] = options.expand
        if options.order_by:
            query_params['$orderby'] = options.order_by
        if options.top:
            query_params['$top'] = options.top
        if options.skip:
            query_params['$skip'] = options.skip
    return query_params