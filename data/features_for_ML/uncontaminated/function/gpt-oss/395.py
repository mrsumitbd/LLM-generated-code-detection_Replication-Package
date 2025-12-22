import torch
import torch.nn as nn
from typing import Any


class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalization."""

    def __init__(self, normalized_shape: int, eps: float = 1e-8, **kwargs: Any):
        super().__init__()
        self.normalized_shape = normalized_shape
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(normalized_shape))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        rms = torch.sqrt(torch.mean(x.pow(2), dim=-1, keepdim=True) + self.eps)
        return x / rms * self.weight


def get_norm_module(
    module: nn.Module,
    causal: bool = False,
    norm: str = "none",
    **norm_kwargs: Any,
) -> nn.Module:
    """
    Return the proper normalization module for the given `module`.

    Parameters
    ----------
    module : nn.Module
        The module for which the normalization is to be created.  The
        normalization will be configured to match the dimensionality of
        this module (e.g. `out_features` for Linear or `out_channels`
        for Conv1d).
    causal : bool, optional
        If ``True`` the returned module must be causal.  Only LayerNorm
        and RMSNorm are considered causal; other normalizations will
        raise a ``ValueError``.
    norm : str, optional
        One of ``"none"``, ``"batch"``, ``"layer"``, ``"group"``,
        ``"instance"``, or ``"rms"``.
    **norm_kwargs
        Additional keyword arguments passed to the normalization
        constructor.

    Returns
    -------
    nn.Module
        The constructed normalization module.

    Raises
    ------
    ValueError
        If an unsupported ``norm`` is requested or if ``causal`` is
        ``True`` but the requested normalization is not causal.
    """
    # Helper to extract the feature dimension from the module
    def _get_features(m: nn.Module) -> int:
        if hasattr(m, "out_features"):
            return m.out_features
        if hasattr(m, "out_channels"):
            return m.out_channels
        raise ValueError(
            f"Cannot infer feature dimension from module of type {type(m).__name__}"
        )

    # Map norm names to constructors
    norm_map = {
        "none": nn.Identity,
        "batch": nn.BatchNorm1d,
        "layer": nn.LayerNorm,
        "group": nn.GroupNorm,
        "instance": nn.InstanceNorm1d,
        "rms": RMSNorm,
    }

    norm = norm.lower()
    if norm not in norm_map:
        raise ValueError(f"Unsupported norm type: {norm!r}")

    # Causal check
    if causal and norm not in {"layer", "rms"}:
        raise ValueError(
            f"Causal normalization requested but {norm!r} does not support causal evaluation"
        )

    # Construct the appropriate normalization
    if norm == "none":
        return nn.Identity()

    # Determine the normalized shape / number of features
    try:
        features = _get_features(module)
    except ValueError as exc:
        raise ValueError(f"Cannot create normalization for module {module!r}") from exc

    if norm == "batch":
        # BatchNorm1d expects num_features
        return nn.BatchNorm1d(features, **norm_kwargs)
    if norm == "layer":
        return nn.LayerNorm(features, **norm_kwargs)
    if norm == "group":
        # GroupNorm requires num_groups and num_channels
        num_groups = norm_kwargs.pop("num_groups", 32)
        return nn.GroupNorm(num_groups, features, **norm_kwargs)
    if norm == "instance":
        return nn.InstanceNorm1d(features, **norm_kwargs)
    if norm == "rms":
        return RMSNorm(features, **norm_kwargs)

    # Fallback (should not reach here)
    raise ValueError(f"Unhandled norm type: {norm!r}")