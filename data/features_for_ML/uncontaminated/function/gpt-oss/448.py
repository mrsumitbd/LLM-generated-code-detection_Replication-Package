import platform
import shutil
import subprocess

def is_supported(cls) -> bool:
    """
    Check if the current system supports seatbelt sandboxing.

    Returns:
        True if the system supports seatbelt (macOS), False otherwise
    """
    # Only macOS (Darwin) supports seatbelt
    if platform.system() != "Darwin":
        return False

    # Ensure the seatbelt binary is available
    if shutil.which("seatbelt") is None:
        return False

    # Verify that the kernel sandbox is enabled
    try:
        output = subprocess.check_output(
            ["sysctl", "-n", "kern.sandbox_enabled"],
            stderr=subprocess.DEVNULL,
        )
        return output.strip() == b"1"
    except Exception:
        return False