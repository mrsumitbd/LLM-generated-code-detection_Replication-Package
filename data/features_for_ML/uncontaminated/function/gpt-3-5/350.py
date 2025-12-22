def _initialize_backend_early(self):
    import os
    import platform

    system = platform.system()
    if system == 'Darwin':
        if 'ARM' in platform.processor():
            os.environ['PYUSB_LIBUSB'] = '/opt/homebrew/lib/libusb-1.0.0.dylib'
        else:
            os.environ['PYUSB_LIBUSB'] = '/usr/local/lib/libusb-1.0.0.dylib'
    elif system == 'Linux':
        os.environ['PYUSB_LIBUSB'] = '/usr/lib/x86_64-linux-gnu/libusb-1.0.so'
    elif system == 'Windows':
        os.environ['PYUSB_LIBUSB'] = 'C:\\Windows\\System32\\libusb-1.0.dll'