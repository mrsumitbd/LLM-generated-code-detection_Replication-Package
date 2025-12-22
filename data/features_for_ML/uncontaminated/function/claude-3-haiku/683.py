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
    generator_type = args.generator_type.lower()

    if generator_type == "random":
        return RandomTopologyGenerator(base_net, **args.generator_params)
    elif generator_type == "grid":
        return GridTopologyGenerator(base_net, **args.generator_params)
    elif generator_type == "radial":
        return RadialTopologyGenerator(base_net, **args.generator_params)
    else:
        raise ValueError(f"Unknown generator type: {args.generator_type}")