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
    generator_type = args.generator.type.lower()
    
    if generator_type == "random":
        return RandomTopologyGenerator(
            base_net=base_net,
            seed=getattr(args.generator, "seed", None),
            **getattr(args.generator, "params", {})
        )
    elif generator_type == "deterministic":
        return DeterministicTopologyGenerator(
            base_net=base_net,
            **getattr(args.generator, "params", {})
        )
    elif generator_type == "evolutionary":
        return EvolutionaryTopologyGenerator(
            base_net=base_net,
            population_size=getattr(args.generator, "population_size", 50),
            generations=getattr(args.generator, "generations", 100),
            mutation_rate=getattr(args.generator, "mutation_rate", 0.1),
            **getattr(args.generator, "params", {})
        )
    elif generator_type == "greedy":
        return GreedyTopologyGenerator(
            base_net=base_net,
            **getattr(args.generator, "params", {})
        )
    else:
        raise ValueError(
            f"Unknown generator type: {generator_type}. "
            f"Supported types are: random, deterministic, evolutionary, greedy"
        )