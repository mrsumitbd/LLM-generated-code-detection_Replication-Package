import platform
import subprocess

def is_supported(cls) -> bool:
        """
        Check if the current system supports seatbelt sandboxing.
        
        Returns:
            True if the system supports seatbelt (macOS), False otherwise
        """
        if platform.system() != "Darwin":
            return False
        
        # Check if sandbox-exec exists
        try:
            subprocess.run(["which", "sandbox-exec"], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False