from typing import Any, Dict

# Import the base class and concrete implementations.
# The actual module names may differ; adjust imports as needed.
try:
    from .topology_generators import (
        TopologyGenerator,
        RandomTopologyGenerator,
        ConnectedTopologyGenerator,
        GridTopologyGenerator,
    )
except Exception:
    # Fallback imports if the module structure is different.
    from topology_generators import (
        TopologyGenerator,
        RandomTopologyGenerator,
        ConnectedTopologyGenerator,
        GridTopologyGenerator,
    )


def _get_generator_type(args: Any) -> str:
    """Extract the generator type from the args namespace."""
    if hasattr(args, "generator_type"):
        return getattr(args, "generator_type")
    if hasattr(args, "generator"):
        gen = getattr(args, "generator")
        if isinstance(gen, dict) and "type" in gen:
            return gen["type"]
        if hasattr(gen, "type"):
            return getattr(gen, "type")
    raise ValueError("Generator type not specified in args.")


def _get_generator_params(args: Any) -> Dict[str, Any]:
    """Extract generator parameters from the args namespace."""
    if hasattr(args, "generator_params"):
        return getattr(args, "generator_params") or {}
    if hasattr(args, "generator"):
        gen = getattr(args, "generator")
        if isinstance(gen, dict) and "params" in gen:
            return gen["params"] or {}
        if hasattr(gen, "params"):
            return getattr(gen, "params") or {}
    return {}


def initialize_topology_generator(
    args: Any,
    base_net: Any,
) -> TopologyGenerator:
    """
    Initialize the appropriate topology generator based on the given arguments.

    Args:
        args: Configuration arguments containing generator type and parameters.
        base_net: Base network to analyze.

    Returns:
        TopologyGenerator: The initialized topology generator.

    Raises:
        ValueError: If the generator type is unknown.
    """
    gen_type = _get_generator_type(args).lower()
    gen_params = _get_generator_params(args)

    if gen_type == "random":
        return RandomTopologyGenerator(base_net, **gen_params)
    if gen_type == "connected":
        return ConnectedTopologyGenerator(base_net, **gen_params)
    if gen_type == "grid":
        return GridTopologyGenerator(base_net, **gen_params)

    raise ValueError(f"Unknown topology generator type: {gen_type}")