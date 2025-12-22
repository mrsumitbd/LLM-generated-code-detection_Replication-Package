import subprocess
from typing import Optional

def merge_base(target_ref: str, base_ref: str = "HEAD") -> Optional[str]:
    """
    Return the merge base commit hash between `target_ref` and `base_ref`.
    If the merge base cannot be determined, return None.
    """
    try:
        result = subprocess.run(
            ["git", "merge-base", target_ref, base_ref],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout.strip() or None
    except subprocess.CalledProcessError:
        return None