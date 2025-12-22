from typing import Any, Dict, Optional, Union, TYPE_CHECKING
from .models import QueryOptions

def build_query_params(options: Optional[QueryOptions] = None) -> dict:
        """Build OData query parameters dict from options

        Args:
            options: Query options to convert

        Returns:
            Dictionary of query parameters
        """
        if not options:
            return {}

        params = {}

        if options.select:
            params["$select"] = ",".join(options.select)

        if options.filter:
            params["$filter"] = options.filter

        if options.expand:
            params["$expand"] = ",".join(options.expand)

        if options.orderby:
            params["$orderby"] = ",".join(options.orderby)

        if options.top is not None:
            params["$top"] = str(options.top)

        if options.skip is not None:
            params["$skip"] = str(options.skip)

        if options.count:
            params["$count"] = "true"

        if options.search:
            params["$search"] = options.search

        return params