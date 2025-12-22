class DatasetFilter:
    """
    Apply allowlist and denylist filters to the DataFrame based on specified column filters.
        - If a allowlist is provided, only keep rows matching the filter values.
        - If a denylist is provided, remove rows matching the filter values.
        - If the filter column does not exist in the DataFrame, the filtering is skipped for that column.
        - Supports Unix shell-style wildcards (``*``, ``?``, ``[seq]``, ``[!seq]``) for string matching.

    This is a utility class that is dataset agnostic and can be used to filter any DataFrame based on the provided
    filter configuration.
    """

    def __init__(self, filter_config: EvalFilterConfig):
        self.filter_config = filter_config

    @staticmethod
    def _match_wildcard_patterns(series: pd.Series, patterns: list[str | int | float]) -> pd.Series:
        import fnmatch
        
        mask = pd.Series([False] * len(series), index=series.index)
        
        for pattern in patterns:
            if isinstance(pattern, str):
                pattern_mask = series.astype(str).apply(lambda x: fnmatch.fnmatch(x, pattern))
                mask = mask | pattern_mask
            else:
                mask = mask | (series == pattern)
        
        return mask

    def apply_filters(self, df) -> pd.DataFrame:
        result_df = df.copy()
        
        # Apply allowlist filters
        if self.filter_config.allowlist:
            for column, values in self.filter_config.allowlist.items():
                if column not in result_df.columns:
                    continue
                
                mask = self._match_wildcard_patterns(result_df[column], values)
                result_df = result_df[mask]
        
        # Apply denylist filters
        if self.filter_config.denylist:
            for column, values in self.filter_config.denylist.items():
                if column not in result_df.columns:
                    continue
                
                mask = self._match_wildcard_patterns(result_df[column], values)
                result_df = result_df[~mask]
        
        return result_df