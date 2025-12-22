def get_differentiable_paths(
    apply_endpoint_fn: Callable, inputs: dict[str, Any], outputs: dict[str, Any]
) -> tuple[list[str], list[str]]:
    """Get the paths of all differentiable leaves present in the given inputs and outputs."""
    import jax
    import jax.numpy as jnp
    from typing import Any, Callable
    
    def is_differentiable(value: Any) -> bool:
        """Check if a value is differentiable (floating point array)."""
        if isinstance(value, jnp.ndarray):
            return jnp.issubdtype(value.dtype, jnp.floating)
        return False
    
    def collect_paths(obj: Any, prefix: str = "") -> list[str]:
        """Recursively collect paths to all differentiable leaves."""
        paths = []
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    paths.extend(collect_paths(value, new_prefix))
                elif isinstance(value, (list, tuple)):
                    paths.extend(collect_paths(value, new_prefix))
                elif is_differentiable(value):
                    paths.append(new_prefix)
        elif isinstance(obj, (list, tuple)):
            for idx, value in enumerate(obj):
                new_prefix = f"{prefix}[{idx}]"
                if isinstance(value, dict):
                    paths.extend(collect_paths(value, new_prefix))
                elif isinstance(value, (list, tuple)):
                    paths.extend(collect_paths(value, new_prefix))
                elif is_differentiable(value):
                    paths.append(new_prefix)
        
        return paths
    
    input_paths = collect_paths(inputs)
    output_paths = collect_paths(outputs)
    
    return (input_paths, output_paths)