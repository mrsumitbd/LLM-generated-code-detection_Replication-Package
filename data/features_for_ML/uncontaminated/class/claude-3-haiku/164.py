from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PIL import Image

class PreviewManager:
    """Manages display generation and frame updates for preview"""

    def __init__(self, config, preview_label: QLabel, text_style):
        self.config = config
        self.preview_label = preview_label
        self.text_style = text_style
        self.display_generator = None
        self.background_image = None
        self.foreground_image = None
        self.foreground_opacity = 1.0
        self.rotation = 0

    def set_device_dimensions(self, width: int, height: int):
        self.display_generator.set_device_dimensions(width, height)

    def initialize_default_background(self, backgrounds_dir: str):
        self.set_background(f"{backgrounds_dir}/default_background.png")

    def determine_background_type(self, file_path):
        pass

    def create_display_generator(self):
        self.display_generator = DisplayGenerator(self.config, self.text_style)

    def update_preview_frame(self):
        image = self.display_generator.generate_preview()
        self.preview_label.setPixmap(self.pil_image_to_qpixmap(image))

    def pil_image_to_qpixmap(self, pil_image):
        return QPixmap.fromImage(pil_image.toqimage())

    def set_background(self, file_path: str):
        self.background_image = Image.open(file_path)
        self.display_generator.set_background(self.background_image)

    def set_foreground(self, file_path: str):
        self.foreground_image = Image.open(file_path)
        self.display_generator.set_foreground(self.foreground_image)

    def set_foreground_opacity(self, opacity: float):
        self.foreground_opacity = opacity
        self.display_generator.set_foreground_opacity(opacity)

    def set_rotation(self, rotation: int):
        self.rotation = rotation
        self.display_generator.set_rotation(rotation)

    def clear_background(self, backgrounds_dir: str):
        self.set_background(f"{backgrounds_dir}/default_background.png")

    def clear_foreground(self):
        self.foreground_image = None
        self.display_generator.set_foreground(None)

    def clear_all(self, backgrounds_dir: str):
        self.clear_background(backgrounds_dir)
        self.clear_foreground()

    def cleanup(self):
        self.display_generator.cleanup()

class DisplayGenerator:
    def __init__(self, config, text_style):
        self.config = config
        self.text_style = text_style

    def set_device_dimensions(self, width: int, height: int):
        pass

    def set_background(self, background_image: Image.Image):
        pass

    def set_foreground(self, foreground_image: Image.Image):
        pass

    def set_foreground_opacity(self, opacity: float):
        pass

    def set_rotation(self, rotation: int):
        pass

    def generate_preview(self) -> Image.Image:
        pass

    def cleanup(self):
        pass