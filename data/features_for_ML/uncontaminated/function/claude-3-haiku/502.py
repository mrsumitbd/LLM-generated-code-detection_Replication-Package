from typing import Optional

class QueryOptions:
    def __init__(self, top: int = None, skip: int = None, order_by: str = None, filter: str = None):
        self.top = top
        self.skip = skip
        self.order_by = order_by
        self.filter = filter

def build_query_params(options: Optional[QueryOptions] = None) -> dict:
    """Build OData query parameters dict from options

    Args:
        options: Query options to convert

    Returns:
        Dictionary of query parameters
    """
    query_params = {}

    if options:
        if options.top is not None:
            query_params['$top'] = options.top
        if options.skip is not None:
            query_params['$skip'] = options.skip
        if options.order_by is not None:
            query_params['$orderby'] = options.order_by
        if options.filter is not None:
            query_params['$filter'] = options.filter

    return query_params