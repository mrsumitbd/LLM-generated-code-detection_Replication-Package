def print_summary(results, functions):
    """
    Print a summary of the benchmark results.
    
    Args:
        results: Dictionary of benchmark results
        functions: List of functions that were benchmarked
    """
    print("\n===== Summary =====")
    
    for env_name, env_results in results.items():
        print(f"\n{env_name}:")
        batch_sizes = env_results['batch_sizes']
        
        # Print function timings
        for func in functions:
            # Skip if this function wasn't benchmarked for this environment
            if func not in env_results['timings'] or not env_results['timings'][func]:
                continue
                
            timings = env_results['timings'][func]
            
            print(f"  {func} times:")
            for i, batch_size in enumerate(batch_sizes):
                if i < len(timings) and timings[i] is not None:
                    print(f"    Batch size {batch_size}: {timings[i]:.4f}s total")
            
            # Print scaling behavior
            if len(batch_sizes) > 1 and all(t is not None for t in timings):
                ideal_scaling = batch_sizes[-1] / batch_sizes[0]
                actual_scaling = timings[-1] / timings[0]
                efficiency = ideal_scaling / actual_scaling
                print(f"    Scaling efficiency (batch {batch_sizes[0]} → {batch_sizes[-1]}): {efficiency:.2f}x")
                
                if efficiency < 0.5:
                    print(f"    ⚠️  Poor scaling for {func}")
                elif efficiency > 0.8:
                    print(f"    ✅ Good scaling for {func}")