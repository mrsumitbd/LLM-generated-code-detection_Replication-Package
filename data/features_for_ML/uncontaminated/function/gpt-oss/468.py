import statistics

def print_summary(results, functions):
    """
    Print a summary of the benchmark results.

    Args:
        results: Dictionary of benchmark results
        functions: List of functions that were benchmarked
    """
    # Header
    print("\nBenchmark Summary")
    print("-" * 80)
    header = f"{'Function':<30} {'Count':>6} {'Mean':>10} {'Std':>10} {'Min':>10} {'Max':>10} {'Median':>10}"
    print(header)
    print("-" * 80)

    for func in functions:
        name = getattr(func, "__name__", str(func))
        data = results.get(name)

        if data is None:
            print(f"{name:<30} {'N/A':>6} {'N/A':>10} {'N/A':>10} {'N/A':>10} {'N/A':>10} {'N/A':>10}")
            continue

        # If data is a dict with precomputed stats
        if isinstance(data, dict):
            count = data.get("count", "N/A")
            mean = data.get("mean", "N/A")
            std = data.get("std", "N/A")
            min_val = data.get("min", "N/A")
            max_val = data.get("max", "N/A")
            median = data.get("median", "N/A")
        # If data is a list/tuple of numeric samples
        elif isinstance(data, (list, tuple)):
            samples = [float(v) for v in data if isinstance(v, (int, float))]
            count = len(samples)
            if count == 0:
                mean = std = min_val = max_val = median = "N/A"
            else:
                mean = statistics.mean(samples)
                std = statistics.stdev(samples) if count > 1 else 0.0
                min_val = min(samples)
                max_val = max(samples)
                median = statistics.median(samples)
        else:
            # Unsupported data type
            print(f"{name:<30} {'N/A':>6} {'N/A':>10} {'N/A':>10} {'N/A':>10} {'N/A':>10} {'N/A':>10}")
            continue

        # Format numeric values
        def fmt(val):
            if isinstance(val, (int, float)):
                return f"{val:10.6g}"
            return f"{val:>10}"

        print(f"{name:<30} {fmt(count)} {fmt(mean)} {fmt(std)} {fmt(min_val)} {fmt(max_val)} {fmt(median)}")
    print("-" * 80)