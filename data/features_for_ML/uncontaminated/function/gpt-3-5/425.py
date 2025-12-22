def profile(repo: str, memory: bool = False, extra_repos: bool = True):
    if memory:
        print(f"Profiling {repo} with memory enabled")
    else:
        print(f"Profiling {repo} with memory disabled")
    
    if extra_repos:
        print("Extra repositories will be included in the profiling")
    else:
        print("Only the specified repository will be profiled")