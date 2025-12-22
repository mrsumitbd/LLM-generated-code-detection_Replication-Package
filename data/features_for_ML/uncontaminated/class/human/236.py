
class OptimizationConfig:
    """Configuration for mathematical optimization."""

    max_workers: int = 4
    use_genetic_algorithm: bool = True
    genetic_population_size: int = 1000
    genetic_generations: int = 200
    genetic_mutation_rate: float = 0.1
    genetic_crossover_rate: float = 0.8
    enable_parallel_processing: bool = True
    max_alternatives: int = 5