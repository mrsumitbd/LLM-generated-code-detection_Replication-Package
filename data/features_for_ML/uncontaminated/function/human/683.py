import warnings
from pandapower import pandapowerNet
from gridfm_datakit.perturbations.topology_perturbation import (
    NMinusKGenerator,
    RandomComponentDropGenerator,
    NoPerturbationGenerator,
    TopologyGenerator,
)

def initialize_topology_generator(
    args: NestedNamespace,
    base_net: pandapowerNet,
) -> TopologyGenerator:
    """Initialize the appropriate topology generator based on the given arguments.

    Args:
        args: Configuration arguments containing generator type and parameters.
        base_net: Base network to analyze.

    Returns:
        TopologyGenerator: The initialized topology generator.

    Raises:
        ValueError: If the generator type is unknown.
    """
    if args.type == "n_minus_k":
        if not hasattr(args, "k"):
            raise ValueError("k parameter is required for n_minus_k generator")
        generator = NMinusKGenerator(args.k, base_net)
        used_args = {"k": args.k, "base_net": base_net}

    elif args.type == "random":
        if not all(hasattr(args, attr) for attr in ["n_topology_variants", "k"]):
            raise ValueError(
                "n_topology_variants and k parameters are required for random generator",
            )
        elements = getattr(args, "elements", ["line", "trafo", "gen", "sgen"])
        generator = RandomComponentDropGenerator(
            args.n_topology_variants,
            args.k,
            base_net,
            elements,
        )
        used_args = {
            "n_topology_variants": args.n_topology_variants,
            "k": args.k,
            "base_net": base_net,
            "elements": elements,
        }

    elif args.type == "none":
        generator = NoPerturbationGenerator()
        used_args = {}

    else:
        raise ValueError(f"Unknown generator type: {args.type}")

    # Check for unused arguments
    unused_args = {
        key: value
        for key, value in args.flatten().items()
        if key not in used_args and key != "type"
    }
    if unused_args:
        warnings.warn(
            f'The following arguments are not used by the topology generator "{args.type}": {unused_args}',
            UserWarning,
        )

    return generator