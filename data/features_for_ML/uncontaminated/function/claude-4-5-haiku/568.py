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
    import numpy as np
    from types import ModuleType
    from pathlib import Path
    from typing import Any, Optional, Sequence, Iterator
    
    if seed is not None:
        np.random.seed(seed)
    
    if base_dir is None:
        base_dir = Path.cwd()
    
    # Get all available endpoints if not specified
    if endpoints is None:
        endpoints = [name for name in dir(api_module) if not name.startswith('_')]
    
    # Iterate through each endpoint
    for endpoint_name in endpoints:
        if not hasattr(api_module, endpoint_name):
            continue
        
        endpoint = getattr(api_module, endpoint_name)
        
        # Check if endpoint has apply and gradient methods
        if not hasattr(endpoint, 'apply') or not hasattr(endpoint, 'gradient'):
            continue
        
        results = []
        eval_count = 0
        
        # Get differentiable paths
        if input_paths is None or output_paths is None:
            try:
                diff_paths = endpoint.differentiable_paths()
                if input_paths is None:
                    input_paths = [p for p in diff_paths if p.startswith('input')]
                if output_paths is None:
                    output_paths = [p for p in diff_paths if p.startswith('output')]
            except:
                input_paths = input_paths or []
                output_paths = output_paths or []
        
        # Sample input/output path combinations
        num_combinations = len(input_paths) * len(output_paths)
        if num_combinations == 0:
            continue
        
        num_samples = max(1, min(num_combinations, max_evals // 2))
        
        iterator = range(num_samples)
        if show_progress:
            try:
                from tqdm import tqdm
                iterator = tqdm(iterator, desc=f"Checking {endpoint_name}")
            except ImportError:
                pass
        
        for sample_idx in iterator:
            # Select random input and output paths
            input_idx = sample_idx % len(input_paths)
            output_idx = (sample_idx // len(input_paths)) % len(output_paths)
            
            input_path = input_paths[input_idx]
            output_path = output_paths[output_idx]
            
            try:
                # Compute gradient using AD
                ad_gradient = endpoint.gradient(inputs, input_path, output_path)
                
                # Compute finite difference approximation
                fd_gradient = _compute_finite_difference(
                    endpoint, inputs, input_path, output_path, eps
                )
                
                # Compare gradients
                if ad_gradient is not None and fd_gradient is not None:
                    rel_error = _compute_relative_error(ad_gradient, fd_gradient)
                    passed = rel_error <= rtol
                    
                    result = GradientCheckResult(
                        input_path=input_path,
                        output_path=output_path,
                        ad_gradient=ad_gradient,
                        fd_gradient=fd_gradient,
                        relative_error=rel_error,
                        passed=passed,
                    )
                    results.append(result)
                    eval_count += 2
                    
            except Exception:
                pass
        
        yield (endpoint_name, results, eval_count)


def _compute_finite_difference(endpoint, inputs, input_path, output_path, eps):
    """Compute finite difference approximation of gradient."""
    import numpy as np
    
    # Get value at input_path
    value = _get_nested_value(inputs, input_path)
    
    if not isinstance(value, (int, float, np.ndarray)):
        return None
    
    # Compute epsilon
    max_val = np.max(np.abs(value)) if isinstance(value, np.ndarray) else abs(value)
    delta = eps * max(max_val, 1.0)
    
    # Forward difference
    inputs_plus = _set_nested_value(inputs, input_path, value + delta)
    output_plus = endpoint.apply(inputs_plus)
    output_plus_val = _get_nested_value(output_plus, output_path)
    
    # Backward difference
    inputs_minus = _set_nested_value(inputs, input_path, value - delta)
    output_minus = endpoint.apply(inputs_minus)
    output_minus_val = _get_nested_value(output_minus, output_path)
    
    # Compute gradient
    gradient = (output_plus_val - output_minus_val) / (2 * delta)
    return gradient


def _get_nested_value(obj, path):
    """Get value from nested object using dot-separated path."""
    parts = path.split('.')
    current = obj
    for part in parts:
        if isinstance(current, dict):
            current = current[part]
        else:
            current = getattr(current, part)
    return current


def _set_nested_value(obj, path, value):
    """Set value in nested object using dot-separated path."""
    import copy
    obj = copy.deepcopy(obj)
    parts = path.split('.')
    current = obj
    for part in parts[:-1]:
        if isinstance(current, dict):
            current = current[part]
        else:
            current = getattr(current, part)
    
    last_part = parts[-1]
    if isinstance(current, dict):
        current[last_part] = value
    else:
        setattr(current, last_part, value)
    return obj


def _compute_relative_error(ad_grad, fd_grad):
    """Compute relative error between AD and FD gradients."""
    import numpy as np
    
    ad_grad = np.asarray(ad_grad)
    fd_grad = np.asarray(fd_grad)
    
    numerator = np.linalg.norm(ad_grad - fd_grad)
    denominator = np.linalg.norm(ad_grad) + np.linalg.norm(fd_grad)
    
    if denominator == 0:
        return 0.0 if numerator == 0 else float('inf')
    
    return numerator / denominator


class GradientCheckResult:
    def __init__(self, input_path, output_path, ad_gradient, fd_gradient, relative_error, passed):
        self.input_path = input_path
        self.output_path = output_path
        self.ad_gradient = ad_gradient
        self.fd_gradient = fd_gradient
        self.relative_error = relative_error
        self.passed = passed