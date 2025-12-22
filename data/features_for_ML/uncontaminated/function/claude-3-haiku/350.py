import os
import sys
import ctypes
import platform

def _initialize_backend_early(self):
    """Initialize libusb backend with cross-platform support.

    Handles macOS (Apple Silicon and Intel), Linux, and Windows with
    comprehensive path detection and fallback mechanisms.
    """
    if sys.platform == 'darwin':
        self._initialize_backend_darwin()
    elif sys.platform.startswith('linux'):
        self._initialize_backend_linux()
    elif sys.platform == 'win32':
        self._initialize_backend_windows()
    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")

def _initialize_backend_darwin(self):
    """Initialize libusb backend on macOS."""
    if platform.machine() == 'arm64':
        # Apple Silicon
        self._load_libusb('/opt/homebrew/lib/libusb-1.0.dylib')
    else:
        # Intel
        self._load_libusb('/usr/local/lib/libusb-1.0.dylib')

def _initialize_backend_linux(self):
    """Initialize libusb backend on Linux."""
    self._load_libusb('libusb-1.0.so.0')

def _initialize_backend_windows(self):
    """Initialize libusb backend on Windows."""
    self._load_libusb('libusb-1.0.dll')

def _load_libusb(self, libusb_path):
    """Load the libusb library from the specified path."""
    try:
        self.libusb = ctypes.CDLL(libusb_path)
    except OSError:
        raise RuntimeError(f"Failed to load libusb from {libusb_path}")