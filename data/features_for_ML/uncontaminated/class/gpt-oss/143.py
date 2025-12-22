from typing import Any, Dict, List, Tuple


class AnalyticsStatisticsService:
    """Service for aggregated statistics and analytics"""

    def _build_filters(self, search_params: Dict[str, Any]) -> List[Tuple[str, Any]]:
        """
        Convert a dictionary of search parameters into a list of filter tuples.

        Each entry in the returned list is a tuple that can be used to build
        query filters. The function supports the following input forms:

        * ``{field: value}`` – simple equality filter.
        * ``{field: {"op": "<operator>", "value": <value>}}`` – custom operator.
          The operator string is preserved in the tuple.

        Parameters
        ----------
        search_params : dict
            Mapping of field names to filter values or operator/value dicts.

        Returns
        -------
        list of tuples
            Each tuple is either ``(field, value)`` for equality filters or
            ``(field, operator, value)`` for custom operators.
        """
        filters: List[Tuple[str, Any]] = []

        for field, value in search_params.items():
            if value is None:
                # Skip parameters that are explicitly set to None
                continue

            if isinstance(value, dict):
                # Expect a dict with keys 'op' and 'value'
                op = value.get("op")
                val = value.get("value")
                if op is not None and val is not None:
                    filters.append((field, op, val))
                else:
                    # Fallback to simple equality if the dict is malformed
                    filters.append((field, value))
            else:
                filters.append((field, value))

        return filters