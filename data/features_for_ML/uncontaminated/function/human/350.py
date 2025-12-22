import platform
import os
import traceback
import usb.core
from config_and_logger import logger
import platform

def _initialize_backend_early(self):
        """Initialize libusb backend with cross-platform support.
        
        Handles macOS (Apple Silicon and Intel), Linux, and Windows with
        comprehensive path detection and fallback mechanisms.
        """
        import platform
        
        error_to_report, local_backend_instance = None, None
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Get the root directory (parent of src/)
            root_dir = os.path.dirname(script_dir)
            system = platform.system()
            
            # Build platform-specific library paths
            if system == "Darwin":  # macOS
                lib_paths_to_try = [
                    "/opt/homebrew/lib/libusb-1.0.dylib",  # Apple Silicon Homebrew
                    "/usr/local/lib/libusb-1.0.dylib",     # Intel Mac Homebrew
                    "/opt/local/lib/libusb-1.0.dylib",     # MacPorts
                    "/usr/lib/libusb-1.0.dylib",           # System location
                ]
            elif system == "Linux":
                lib_paths_to_try = [
                    "/usr/lib/x86_64-linux-gnu/libusb-1.0.so",  # Ubuntu/Debian x64
                    "/usr/lib/aarch64-linux-gnu/libusb-1.0.so", # Ubuntu/Debian ARM64
                    "/usr/lib64/libusb-1.0.so",                  # RHEL/CentOS/Fedora x64
                    "/usr/lib/libusb-1.0.so",                    # Generic location
                    "/usr/local/lib/libusb-1.0.so",              # Compiled from source
                ]
            elif system == "Windows":
                lib_paths_to_try = (
                    [os.path.join(root_dir, name) for name in ["libusb-1.0.dll"]]  # Look in root directory
                    + [os.path.join(root_dir, "MS64", "dll", name) for name in ["libusb-1.0.dll"]]
                    + [os.path.join(root_dir, "MS32", "dll", name) for name in ["libusb-1.0.dll"]]
                    + [os.path.join(root_dir, "lib", name) for name in ["libusb-1.0.dll"]]
                )
            else:
                # Unknown system - try generic paths
                lib_paths_to_try = []
                logger.warning(
                    "GUI",
                    "_initialize_backend_early",
                    f"Unknown system '{system}', will try system paths only.",
                )
            
            # Try to find the library in the specified paths
            lib_path = next((p for p in lib_paths_to_try if os.path.exists(p)), None)
            
            if not lib_path:
                logger.warning(
                    "GUI",
                    "_initialize_backend_early",
                    f"libusb library not found in expected {system} paths. Trying system paths.",
                )
                # Fallback to system paths
                local_backend_instance = usb.backend.libusb1.get_backend()
                if not local_backend_instance:
                    error_to_report = f"Libusb backend failed from system paths on {system}."
            else:
                logger.info(
                    "GUI",
                    "_initialize_backend_early",
                    f"Found libusb library at: {lib_path}",
                )
                # Use the found library path
                local_backend_instance = usb.backend.libusb1.get_backend(find_library=lambda x: lib_path)
                if not local_backend_instance:
                    error_to_report = f"Failed to initialize backend with library: {lib_path}. Check architecture compatibility."
            
            if error_to_report:
                logger.error("GUI", "_initialize_backend_early", error_to_report)
                return False, error_to_report, None
                
            logger.info(
                "GUI",
                "_initialize_backend_early",
                f"Backend initialized successfully: {local_backend_instance}",
            )
            return True, None, local_backend_instance
            
        except (
            OSError,
            usb.core.USBError,
            RuntimeError,
            AttributeError,
            ImportError,
        ) as e:
            error_to_report = f"Unexpected error initializing libusb on {platform.system()}: {e}"
            logger.error(
                "GUI",
                "_initialize_backend_early",
                f"{error_to_report}\n{traceback.format_exc()}",
            )
            return False, error_to_report, None