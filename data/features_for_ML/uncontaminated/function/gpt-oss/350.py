def _initialize_backend_early(self):
    """
    Initialize libusb backend with cross-platform support.
    Handles macOS (Apple Silicon and Intel), Linux, and Windows with
    comprehensive path detection and fallback mechanisms.
    """
    import os
    import sys
    import platform
    import ctypes.util

    try:
        from usb.backend import libusb1
    except Exception as exc:
        raise RuntimeError("pyusb is required to initialize the libusb backend") from exc

    libusb_path = None

    # Detect platform and build candidate paths
    if sys.platform == "darwin":
        # macOS
        arch = platform.machine()
        if arch == "arm64":
            # Apple Silicon
            candidates = [
                "/opt/homebrew/lib/libusb-1.0.dylib",
                "/usr/local/lib/libusb-1.0.dylib",
                "/usr/lib/libusb-1.0.dylib",
            ]
        else:
            # Intel
            candidates = [
                "/usr/local/lib/libusb-1.0.dylib",
                "/usr/lib/libusb-1.0.dylib",
            ]
        for path in candidates:
            if os.path.exists(path):
                libusb_path = path
                break
        if libusb_path is None:
            libusb_path = ctypes.util.find_library("usb-1.0")

    elif sys.platform.startswith("linux"):
        # Linux
        candidates = [
            "/usr/lib/x86_64-linux-gnu/libusb-1.0.so.0",
            "/usr/lib/libusb-1.0.so.0",
            "/usr/local/lib/libusb-1.0.so.0",
        ]
        for path in candidates:
            if os.path.exists(path):
                libusb_path = path
                break
        if libusb_path is None:
            libusb_path = ctypes.util.find_library("usb-1.0")

    elif sys.platform == "win32":
        # Windows
        # Try the directory of this module first
        try:
            module_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            module_dir = os.getcwd()
        candidates = [os.path.join(module_dir, "libusb-1.0.dll")]
        for path in candidates:
            if os.path.exists(path):
                libusb_path = path
                break
        if libusb_path is None:
            libusb_path = ctypes.util.find_library("usb-1.0")

    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")

    # Attempt to load the backend
    try:
        if libusb_path:
            self.backend = libusb1.get_backend(libusb_path=libusb_path)
        else:
            # Let libusb1 find the default library
            self.backend = libusb1.get_backend()
    except Exception as exc:
        raise RuntimeError(f"Failed to initialize libusb backend: {exc}") from exc