class AnalyticsStatisticsService:
    """Service for aggregated statistics and analytics"""

    def _build_filters(self, search_params: Dict[str, Any]) -> List:
        """
        Build a list of filters from search parameters.
        
        Args:
            search_params: Dictionary containing search parameters
            
        Returns:
            List of filter conditions
        """
        filters = []
        
        if not search_params:
            return filters
        
        # Handle date range filters
        if 'start_date' in search_params and search_params['start_date']:
            filters.append({
                'field': 'date',
                'operator': 'gte',
                'value': search_params['start_date']
            })
        
        if 'end_date' in search_params and search_params['end_date']:
            filters.append({
                'field': 'date',
                'operator': 'lte',
                'value': search_params['end_date']
            })
        
        # Handle status filter
        if 'status' in search_params and search_params['status']:
            filters.append({
                'field': 'status',
                'operator': 'eq',
                'value': search_params['status']
            })
        
        # Handle category filter
        if 'category' in search_params and search_params['category']:
            filters.append({
                'field': 'category',
                'operator': 'eq',
                'value': search_params['category']
            })
        
        # Handle user_id filter
        if 'user_id' in search_params and search_params['user_id']:
            filters.append({
                'field': 'user_id',
                'operator': 'eq',
                'value': search_params['user_id']
            })
        
        # Handle tags filter (can be multiple)
        if 'tags' in search_params and search_params['tags']:
            tags = search_params['tags']
            if isinstance(tags, list):
                filters.append({
                    'field': 'tags',
                    'operator': 'in',
                    'value': tags
                })
            else:
                filters.append({
                    'field': 'tags',
                    'operator': 'contains',
                    'value': tags
                })
        
        # Handle search query
        if 'query' in search_params and search_params['query']:
            filters.append({
                'field': 'text',
                'operator': 'contains',
                'value': search_params['query']
            })
        
        # Handle numeric range filters
        if 'min_value' in search_params and search_params['min_value'] is not None:
            filters.append({
                'field': 'value',
                'operator': 'gte',
                'value': search_params['min_value']
            })
        
        if 'max_value' in search_params and search_params['max_value'] is not None:
            filters.append({
                'field': 'value',
                'operator': 'lte',
                'value': search_params['max_value']
            })
        
        # Handle custom filters
        if 'filters' in search_params and isinstance(search_params['filters'], list):
            filters.extend(search_params['filters'])
        
        return filters