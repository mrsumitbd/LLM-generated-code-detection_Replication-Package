def merge_base(target_ref: str, base_ref: str = "HEAD"):
    import subprocess
    
    try:
        result = subprocess.run(
            ["git", "merge-base", base_ref, target_ref],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return None