def print_summary(results, functions):
    """
    Print a summary of the benchmark results.
    
    Args:
        results: Dictionary of benchmark results
        functions: List of functions that were benchmarked
    """
    print("Benchmark Results Summary:")
    print("-" * 30)
    
    for func in functions:
        print(f"Function: {func.__name__}")
        print(f"  Mean time: {results[func]['mean']:.6f} seconds")
        print(f"  Median time: {results[func]['median']:.6f} seconds")
        print(f"  Standard deviation: {results[func]['std']:.6f} seconds")
        print()