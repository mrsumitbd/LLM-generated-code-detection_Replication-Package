import os
import tempfile

def rules_dir_writable() -> bool:
    """
    Checks if Prometheus rules directory is writable.
    The default Prometheus rules directory is assumed to be
    '/etc/prometheus/rules'. If the directory does not exist or is not
    writable, the function returns False.
    """
    rules_dir = "/etc/prometheus/rules"

    # Ensure the directory exists
    if not os.path.isdir(rules_dir):
        return False

    # Quick check using os.access
    if os.access(rules_dir, os.W_OK):
        return True

    # Fallback: try to create a temporary file in the directory
    try:
        with tempfile.NamedTemporaryFile(dir=rules_dir, delete=True):
            return True
    except Exception:
        return False