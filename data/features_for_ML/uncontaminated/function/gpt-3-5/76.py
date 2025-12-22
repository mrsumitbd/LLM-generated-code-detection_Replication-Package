def merge_base(target_ref: str, base_ref: str = "HEAD"):
    import subprocess
    
    try:
        subprocess.run(["git", "merge-base", target_ref, base_ref], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")