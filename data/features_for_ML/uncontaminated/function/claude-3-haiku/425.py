def profile(repo: str, memory: bool = False, extra_repos: bool = True):
    import os
    import subprocess

    # Check if the repository exists
    if not os.path.exists(repo):
        print(f"Error: Repository '{repo}' does not exist.")
        return

    # Change to the repository directory
    os.chdir(repo)

    # Run the profiling command
    if memory:
        subprocess.run(["python", "-m", "memory_profiler", "main.py"], check=True)
    else:
        subprocess.run(["python", "-m", "cProfile", "-s", "time", "main.py"], check=True)

    # Check for additional repositories
    if extra_repos:
        for dir_name in os.listdir(os.path.dirname(repo)):
            if os.path.isdir(os.path.join(os.path.dirname(repo), dir_name)) and dir_name != os.path.basename(repo):
                print(f"Additional repository found: {dir_name}")
                profile(os.path.join(os.path.dirname(repo), dir_name), memory, extra_repos)