def print_summary(results, functions):
    print("Benchmark Results Summary:")
    for func in functions:
        print(f"Function: {func}")
        print(f"Average Time: {results[func]['average_time']} seconds")
        print(f"Min Time: {results[func]['min_time']} seconds")
        print(f"Max Time: {results[func]['max_time']} seconds")
        print(f"Total Runs: {results[func]['total_runs']}")
        print()