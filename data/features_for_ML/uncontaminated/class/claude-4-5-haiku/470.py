class UIBase:

    def __init__(self, ui_path):
        self.ui_path = ui_path
        self.window = None
        self.width = 800
        self.height = 600
        self.device_pixel_ratio = 1.0
        self.scale_override = 1.0
        self.macro_information = {}

    def resize_window(self, width, height, device_pixel_ratio=None):
        self.width = width
        self.height = height
        if device_pixel_ratio is not None:
            self.device_pixel_ratio = device_pixel_ratio
        if self.window:
            self.window.resize(width, height)

    def get_macro_information(self):
        return self.macro_information

    def get_scale_override(self):
        return self.scale_override

    def stop_window(self):
        if self.window:
            self.window.close()
            self.window = None

    def create_window(self):
        self.window = {
            'width': self.width,
            'height': self.height,
            'device_pixel_ratio': self.device_pixel_ratio,
            'ui_path': self.ui_path
        }
        return self.window