def initialize_topology_generator(args: NestedNamespace, base_net: pandapowerNet) -> TopologyGenerator:
    if args.generator_type == 'type1':
        return TopologyGeneratorType1(args, base_net)
    elif args.generator_type == 'type2':
        return TopologyGeneratorType2(args, base_net)
    else:
        raise ValueError("Unknown generator type")