def merge_base(target_ref: str, base_ref: str = "HEAD"):
    import subprocess

    try:
        output = subprocess.check_output(["git", "merge-base", target_ref, base_ref], universal_newlines=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        return None