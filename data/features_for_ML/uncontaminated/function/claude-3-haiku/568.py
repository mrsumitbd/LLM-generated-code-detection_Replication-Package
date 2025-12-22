from typing import ModuleType, Any, Optional, Sequence, Iterator
from pathlib import Path
from dataclasses import dataclass
from tqdm import tqdm
import numpy as np
import jax
import jax.numpy as jnp

@dataclass
class GradientCheckResult:
    path: str
    expected: jnp.ndarray
    actual: jnp.ndarray
    relative_error: float

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
    if seed is not None:
        jax.random.seed(seed)

    if input_paths is None:
        input_paths = list(inputs.keys())

    if output_paths is None:
        output_paths = list(inputs.keys())

    if endpoints is None:
        endpoints = [name for name in dir(api_module) if name.endswith("AD")]

    for endpoint_name in endpoints:
        endpoint = getattr(api_module, endpoint_name)
        grad_fn = jax.grad(endpoint, argnums=list(range(len(input_paths))))
        results = []

        for _ in tqdm(range(max_evals), disable=not show_progress):
            input_values = {path: jnp.array(inputs[path]) for path in input_paths}
            output_values = endpoint(**input_values)

            grads = grad_fn(**input_values)
            for i, output_path in enumerate(output_paths):
                expected = grads[i]
                actual = jax.api._check_grads_impl(
                    lambda *args: endpoint(**{p: a for p, a in zip(input_paths, args)})[output_path],
                    input_values.values(),
                    eps=eps,
                )
                relative_error = jnp.max(jnp.abs((expected - actual) / (jnp.abs(expected) + 1e-8)))
                results.append(GradientCheckResult(output_path, expected, actual, relative_error))

        yield endpoint_name, results, max_evals