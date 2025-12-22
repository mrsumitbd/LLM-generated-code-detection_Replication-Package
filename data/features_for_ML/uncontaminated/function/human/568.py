from collections.abc import Iterator, Sequence
from types import ModuleType
from pathlib import Path
from typing import (
    Any,
    Callable,
    Literal,
    NamedTuple,
    Optional,
    get_args,
)
import numpy as np
from .core import create_endpoints

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
    """Check gradients of endpoints against a finite difference approximation.

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
    # We apply a global cache to these functions to avoid hashing `inputs` multiple times,
    # so we need to clear the cache before each run.
    _jacobian_via_apply.clear_cache()
    _jacobian_via_jacobian.clear_cache()
    _jacobian_via_jvp.clear_cache()
    _jacobian_via_vjp.clear_cache()

    # Get available endpoints
    endpoint_functions = {func.__name__: func for func in create_endpoints(api_module)}
    available_endpoints = [
        func_name
        for func_name in endpoint_functions
        if func_name in get_args(ADEndpointName)
    ]

    if not available_endpoints:
        raise ValueError(f"No AD endpoints found in {api_module.__name__}")

    if not endpoints:
        endpoints = available_endpoints

    for endpoint in endpoints:
        if endpoint not in available_endpoints:
            raise ValueError(f"Endpoint {endpoint} not found in {api_module.__name__}")

    # Load + dump inputs to ensure they are valid + normalized
    InputSchema = get_input_schema(endpoint_functions["apply"])
    loaded_inputs = InputSchema.model_validate(inputs, context={"base_dir": base_dir})
    inputs = loaded_inputs.inputs.model_dump()
    outputs = endpoint_functions["apply"](loaded_inputs).model_dump()

    # Get differentiable paths
    diff_inputs, diff_outputs = get_differentiable_paths(
        endpoint_functions["apply"],
        inputs,
        outputs,
    )

    if not input_paths:
        input_paths = diff_inputs

    for path in input_paths:
        if path not in diff_inputs:
            raise ValueError(
                f"Input path {path} not found in differentiable paths ({diff_inputs})"
            )

    if not output_paths:
        output_paths = diff_outputs

    for path in output_paths:
        if path not in diff_outputs:
            raise ValueError(
                f"Output path {path} not found in differentiable paths ({diff_outputs})"
            )

    # Check gradients for each endpoint separately
    rng = np.random.RandomState(seed)

    for endpoint in endpoints:
        failures, num_evals = check_endpoint_gradients(
            endpoint_functions,
            inputs,
            endpoint,
            diff_inputs=input_paths,
            diff_outputs=output_paths,
            max_evals=max_evals,
            eps=eps,
            rtol=rtol,
            rng=rng,
            show_progress=show_progress,
        )
        yield endpoint, failures, num_evals