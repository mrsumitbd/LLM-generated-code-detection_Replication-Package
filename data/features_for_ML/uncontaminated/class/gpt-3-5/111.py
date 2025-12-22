import pandas as pd
from typing import List

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
    def _match_wildcard_patterns(series: pd.Series, patterns: List[str | int | float]) -> pd.Series:
        pass

    def apply_filters(self, df) -> pd.DataFrame:
        for column, filters in self.filter_config.items():
            if column in df.columns:
                if 'allowlist' in filters:
                    df = df[df[column].isin(filters['allowlist'])]
                if 'denylist' in filters:
                    df = df[~df[column].isin(filters['denylist'])]
        return df