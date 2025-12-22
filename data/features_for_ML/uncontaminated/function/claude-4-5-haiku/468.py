def print_summary(results, functions):
    """
    Print a summary of the benchmark results.
    
    Args:
        results: Dictionary of benchmark results
        functions: List of functions that were benchmarked
    """
    print("\n" + "="*60)
    print("BENCHMARK SUMMARY")
    print("="*60)
    
    if not results:
        print("No results to display.")
        return
    
    # Find the maximum function name length for alignment
    max_name_len = max(len(func.__name__) for func in functions) if functions else 0
    max_name_len = max(max_name_len, len("Function"))
    
    # Print header
    print(f"{'Function':<{max_name_len}} | {'Min (s)':<12} | {'Max (s)':<12} | {'Mean (s)':<12} | {'Std Dev':<12}")
    print("-" * (max_name_len + 60))
    
    # Print results for each function
    for func in functions:
        func_name = func.__name__
        if func_name in results:
            times = results[func_name]
            if times:
                min_time = min(times)
                max_time = max(times)
                mean_time = sum(times) / len(times)
                
                # Calculate standard deviation
                variance = sum((t - mean_time) ** 2 for t in times) / len(times)
                std_dev = variance ** 0.5
                
                print(f"{func_name:<{max_name_len}} | {min_time:<12.6f} | {max_time:<12.6f} | {mean_time:<12.6f} | {std_dev:<12.6f}")
    
    print("="*60 + "\n")