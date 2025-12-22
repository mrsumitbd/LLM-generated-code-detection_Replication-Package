import pandas as pd
from fnmatch import fnmatch

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
        """
        Apply Unix shell-style wildcard patterns to a pandas Series.

        Args:
            series (pd.Series): The input series to be filtered.
            patterns (list[str | int | float]): The list of wildcard patterns to match against the series.

        Returns:
            pd.Series: A boolean series indicating which rows match the wildcard patterns.
        """
        return series.apply(lambda x: any(fnmatch(str(x), str(pattern)) for pattern in patterns))

    def apply_filters(self, df) -> pd.DataFrame:
        """
        Apply the allowlist and denylist filters to the input DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame to be filtered.

        Returns:
            pd.DataFrame: The filtered DataFrame.
        """
        for column, filters in self.filter_config.allowlist.items():
            if column in df.columns:
                df = df[self._match_wildcard_patterns(df[column], filters)]

        for column, filters in self.filter_config.denylist.items():
            if column in df.columns:
                df = df[~self._match_wildcard_patterns(df[column], filters)]

        return df