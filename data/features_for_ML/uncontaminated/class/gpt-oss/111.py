import pandas as pd
import fnmatch
from typing import Any, Dict, List, Union


class EvalFilterConfig:
    """
    Minimal configuration holder for DatasetFilter.
    Expected to have two optional attributes:
        - allowlist: Dict[str, List[Union[str, int, float]]]
        - denylist:  Dict[str, List[Union[str, int, float]]]
    """
    def __init__(
        self,
        allowlist: Dict[str, List[Union[str, int, float]]] | None = None,
        denylist: Dict[str, List[Union[str, int, float]]] | None = None,
    ):
        self.allowlist = allowlist or {}
        self.denylist = denylist or {}


class DatasetFilter:
    """
    Apply allowlist and denylist filters to the DataFrame based on specified column filters.
        - If a allowlist is provided, only keep rows matching the filter values.
        - If a denylist is provided, remove rows matching the filter values.
        - If the filter column does not exist in the DataFrame, the filtering is skipped for that column.
        - Supports Unix shell-style wildcards (``*``, ``?``, ``[seq]``, ``[!seq]``) for string matching.
    """

    def __init__(self, filter_config: EvalFilterConfig):
        self.filter_config = filter_config

    @staticmethod
    def _match_wildcard_patterns(
        series: pd.Series, patterns: List[Union[str, int, float]]
    ) -> pd.Series:
        """
        Return a boolean mask where each element is True if the corresponding
        series value matches any of the provided patterns.
        """
        if series.empty or not patterns:
            return pd.Series([False] * len(series), index=series.index)

        # Prepare mask
        mask = pd.Series([False] * len(series), index=series.index)

        # Determine if series is string-like
        is_str_series = series.dtype.kind in {"O", "U", "S"}

        for pat in patterns:
            if isinstance(pat, str) and is_str_series:
                # Use fnmatch for wildcard matching
                # Convert series to string for comparison
                str_series = series.astype(str)
                # fnmatch.fnmatchcase works element-wise
                mask |= str_series.apply(lambda x: fnmatch.fnmatchcase(x, pat))
            else:
                # Direct equality comparison for non-string or non-string series
                mask |= series == pat

        return mask

    def apply_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply allowlist and denylist filters to the DataFrame.
        """
        result = df.copy()

        # Apply allowlist filters
        for col, patterns in self.filter_config.allowlist.items():
            if col not in result.columns:
                continue
            mask = self._match_wildcard_patterns(result[col], patterns)
            result = result[mask]

        # Apply denylist filters
        for col, patterns in self.filter_config.denylist.items():
            if col not in result.columns:
                continue
            mask = self._match_wildcard_patterns(result[col], patterns)
            result = result[~mask]

        return result