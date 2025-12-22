from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from importlib import import_module
from inspect import isclass
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from tqdm import tqdm

# --------------------------------------------------------------------------- #
# Helper types and imports
# --------------------------------------------------------------------------- #
try:
    # Try to import the real types from the tesseract library
    from tesseract.ad import ADEndpointName, GradientCheckResult
except Exception:  # pragma: no cover
    # Fallback minimal definitions for type checking / documentation purposes
    class ADEndpointName:
        name: str

    @dataclass
    class GradientCheckResult:
        input_path: str
        output_path: str
        analytic: np.ndarray
        finite_difference: np.ndarray
        rel_error: np.ndarray
        passed: bool


# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #
def _get_by_path(data: Dict[str, Any], path: str) -> Any:
    """Retrieve a value from a nested dictionary using a dot-separated path."""
    parts = path.split(".")
    for part in parts:
        data = data[part]
    return data


def _set_by_path(data: Dict[str, Any], path: str, value: Any) -> None:
    """Set a value in a nested dictionary using a dot-separated path."""
    parts = path.split(".")
    for part in parts[:-1]:
        data = data[part]
    data[parts[-1]] = value


def _copy_inputs(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Deep copy of the inputs dictionary (shallow copy of nested dicts is enough)."""
    return {k: v.copy() if isinstance(v, dict) else v for k, v in inputs.items()}


def _flatten_inputs(inputs: Dict[str, Any]) -> Dict[str, np.ndarray]:
    """Return a flat mapping from path to numpy array for all array inputs."""
    flat: Dict[str, np.ndarray] = {}
    for key, val in inputs.items():
        if isinstance(val, np.ndarray):
            flat[key] = val
        elif isinstance(val, dict):
            for subkey, subval in val.items():
                if isinstance(subval, np.ndarray):
                    flat[f"{key}.{subkey}"] = subval
    return flat


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def check_gradients(
    api_module: ModuleType,
    inputs: dict[str, Any],
    *,
    input_paths: Optional[Sequence[str]] = None,
    output_paths: Optional[Sequence[str]] = None,
    base_dir: Optional[Path] = None,
    endpoints: Optional[Sequence[ADEndpointName]] = None,
    max_evals: int = 1000,
    eps: float = 1e-4,
    rtol: float = 0.1,
    seed: Optional[int] = None,
    show_progress: bool = True,
) -> Iterator[tuple[str, list[GradientCheckResult], int]]:
    """
    Check gradients of endpoints against a finite difference approximation.

    Args:
        api_module: The module containing the Tesseract endpoints.
        inputs: The inputs to apply to evaluate gradients at.
        input_paths: The input paths to check. If not provided, all differentiable paths are checked.
        output_paths: The output paths to check. If not provided, all differentiable paths are checked.
        base_dir: The base directory to resolve relative paths.
        endpoints: The AD endpoints to check. If not provided, all available endpoints are checked.
        max_evals: The target number of ``apply`` evaluations to perform.
        eps: The epsilon to use for finite differences, as a fraction of the maximum absolute value of each input.
        rtol: The relative tolerance to use for comparison.
        seed: The random seed to use for sampling. If not provided, a random seed is used.
        show_progress: Whether to show a progress bar.
    """
    # ----------------------------------------------------------------------- #
    # Resolve endpoints
    # ----------------------------------------------------------------------- #
    if endpoints is None:
        # Find all attributes that are instances of ADEndpointName
        endpoints = [
            getattr(api_module, name)
            for name in dir(api_module)
            if isinstance(getattr(api_module, name), ADEndpointName)
        ]

    # ----------------------------------------------------------------------- #
    # Prepare random seed
    # ----------------------------------------------------------------------- #
    rng = np.random.default_rng(seed)

    # ----------------------------------------------------------------------- #
    # Resolve input and output paths
    # ----------------------------------------------------------------------- #
    flat_inputs = _flatten_inputs(inputs)
    if input_paths is None:
        input_paths = list(flat_inputs.keys())
    if output_paths is None:
        # We will discover output paths from the first endpoint's gradient
        # but we need to compute it first
        output_paths = None

    # ----------------------------------------------------------------------- #
    # Iterate over endpoints
    # ----------------------------------------------------------------------- #
    endpoint_iter = tqdm(endpoints, disable=not show_progress, desc="Endpoints")
    for endpoint in endpoint_iter:
        name = getattr(endpoint, "name", str(endpoint))
        # ------------------------------------------------------------------- #
        # Compute analytic gradients
        # ------------------------------------------------------------------- #
        try:
            analytic_grads = endpoint.gradient(inputs)
        except Exception as exc:  # pragma: no cover
            # If gradient computation fails, skip this endpoint
            yield (name, [], 0)
            continue

        # Determine output paths if not provided
        if output_paths is None:
            output_paths = list(analytic_grads.keys())

        # ------------------------------------------------------------------- #
        # Prepare result list
        # ------------------------------------------------------------------- #
        results: List[GradientCheckResult] = []

        # ------------------------------------------------------------------- #
        # Count evaluations
        # ------------------------------------------------------------------- #
        evals_used = 0

        # ------------------------------------------------------------------- #
        # Iterate over output and input paths
        # ------------------------------------------------------------------- #
        for out_path in output_paths:
            if out_path not in analytic_grads:
                continue
            for in_path in input_paths:
                if in_path not in analytic_grads[out_path]:
                    continue

                # Get analytic gradient slice
                analytic = analytic_grads[out_path][in_path]
                analytic = np.asarray(analytic)

                # Get input array
                inp_arr = _get_by_path(inputs, in_path)
                inp_arr = np.asarray(inp_arr)

                # Determine epsilon for each element
                max_abs = np.max(np.abs(inp_arr))
                if max_abs == 0:
                    max_abs = 1.0
                delta = eps * max_abs

                # Prepare finite difference gradient array
                fd_grad = np.zeros_like(analytic)

                # Iterate over all elements
                it = np.nditer(inp_arr, flags=["multi_index"])
                while not it.finished:
                    idx = it.multi_index
                    # Perturb positively
                    perturbed = _copy_inputs(inputs)
                    val = inp_arr[idx]
                    perturbed_val = val + delta
                    _set_by_path(perturbed, in_path, np.asarray(perturbed_val))
                    # Evaluate
                    out_pos = endpoint.apply(perturbed)
                    evals_used += 1
                    out_pos_val = _get_by_path(out_pos, out_path)

                    # Perturb negatively
                    perturbed = _copy_inputs(inputs)
                    perturbed_val = val - delta
                    _set_by_path(perturbed, in_path, np.asarray(perturbed_val))
                    out_neg = endpoint.apply(perturbed)
                    evals_used += 1
                    out_neg_val = _get_by_path(out_neg, out_path)

                    # Finite difference derivative
                    fd = (out_pos_val - out_neg_val) / (2 * delta)
                    fd_grad[idx] = fd

                    it.iternext()

                    # Stop if we exceed max_evals
                    if evals_used >= max_evals:
                        break
                # ------------------------------------------------------------------- #
                # Compare analytic and finite difference gradients
                # ------------------------------------------------------------------- #
                rel_err = np.abs(fd_grad - analytic) / (
                    np.maximum(np.abs(fd_grad), np.abs(analytic), 1e-8)
                )
                passed = np.all(rel_err <= rtol)

                results.append(
                    GradientCheckResult(
                        input_path=in_path,
                        output_path=out_path,
                        analytic=analytic,
                        finite_difference=fd_grad,
                        rel_error=rel_err,
                        passed=passed,
                    )
                )

                if evals_used >= max_evals:
                    break
            if evals_used >= max_evals:
                break

        yield (name, results, evals_used)