def _initialize_backend_early(self):
    """Initialize libusb backend with cross-platform support.
    
    Handles macOS (Apple Silicon and Intel), Linux, and Windows with
    comprehensive path detection and fallback mechanisms.
    """
    import os
    import sys
    import platform
    from pathlib import Path
    
    system = platform.system()
    machine = platform.machine()
    
    libusb_paths = []
    
    if system == "Darwin":  # macOS
        homebrew_paths = [
            "/opt/homebrew/lib",  # Apple Silicon
            "/usr/local/lib",      # Intel
        ]
        
        macports_paths = [
            "/opt/local/lib",
        ]
        
        common_paths = [
            "/usr/local/opt/libusb/lib",
            "/opt/homebrew/opt/libusb/lib",
        ]
        
        libusb_paths.extend(homebrew_paths + macports_paths + common_paths)
        
        # Add architecture-specific paths
        if machine == "arm64":
            libusb_paths.extend([
                "/opt/homebrew/lib",
                "/opt/homebrew/opt/libusb/lib",
            ])
        else:
            libusb_paths.extend([
                "/usr/local/lib",
                "/usr/local/opt/libusb/lib",
            ])
    
    elif system == "Linux":
        libusb_paths.extend([
            "/usr/lib",
            "/usr/local/lib",
            "/usr/lib/x86_64-linux-gnu",
            "/usr/lib/aarch64-linux-gnu",
            "/usr/lib/arm-linux-gnueabihf",
            "/lib",
            "/lib/x86_64-linux-gnu",
            "/lib/aarch64-linux-gnu",
        ])
        
        # Add LD_LIBRARY_PATH
        ld_library_path = os.environ.get("LD_LIBRARY_PATH", "")
        if ld_library_path:
            libusb_paths.extend(ld_library_path.split(":"))
    
    elif system == "Windows":
        libusb_paths.extend([
            os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "System32"),
            os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "SysWOW64"),
            "C:\\Program Files\\libusb",
            "C:\\Program Files (x86)\\libusb",
        ])
    
    # Remove duplicates and non-existent paths
    libusb_paths = list(dict.fromkeys(libusb_paths))
    libusb_paths = [p for p in libusb_paths if os.path.isdir(p)]
    
    # Try to find and load libusb
    libusb_names = []
    if system == "Darwin":
        libusb_names = ["libusb-1.0.dylib", "libusb.dylib"]
    elif system == "Linux":
        libusb_names = ["libusb-1.0.so.0", "libusb-1.0.so", "libusb.so"]
    elif system == "Windows":
        libusb_names = ["libusb-1.0.dll", "libusb0.dll", "libusb.dll"]
    
    # Store paths for later use
    self._libusb_paths = libusb_paths
    self._libusb_names = libusb_names
    self._system = system
    self._machine = machine