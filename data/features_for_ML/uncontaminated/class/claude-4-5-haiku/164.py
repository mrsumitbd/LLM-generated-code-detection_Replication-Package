from PIL import Image
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel
import io
import os


class PreviewManager:
    """Manages display generation and frame updates for preview"""

    def __init__(self, config, preview_label: QLabel, text_style):
        self.config = config
        self.preview_label = preview_label
        self.text_style = text_style
        self.device_width = 1080
        self.device_height = 1920
        self.background_image = None
        self.background_type = None
        self.foreground_image = None
        self.foreground_opacity = 1.0
        self.rotation = 0
        self.display_generator = None

    def set_device_dimensions(self, width: int, height: int):
        self.device_width = width
        self.device_height = height

    def initialize_default_background(self, backgrounds_dir: str):
        default_bg_path = os.path.join(backgrounds_dir, "default.png")
        if os.path.exists(default_bg_path):
            self.set_background(default_bg_path)
        else:
            self.background_image = Image.new('RGB', (self.device_width, self.device_height), color='white')
            self.background_type = 'color'

    def determine_background_type(self, file_path):
        if not file_path:
            return None
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
            return 'video'
        elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
            return 'image'
        return None

    def create_display_generator(self):
        if self.background_type == 'video':
            from display_generator import VideoDisplayGenerator
            self.display_generator = VideoDisplayGenerator(
                self.config,
                self.background_image,
                self.foreground_image,
                self.foreground_opacity,
                self.rotation,
                self.device_width,
                self.device_height
            )
        else:
            from display_generator import ImageDisplayGenerator
            self.display_generator = ImageDisplayGenerator(
                self.config,
                self.background_image,
                self.foreground_image,
                self.foreground_opacity,
                self.rotation,
                self.device_width,
                self.device_height
            )

    def update_preview_frame(self):
        if self.display_generator is None:
            self.create_display_generator()
        
        frame = self.display_generator.get_frame()
        if frame is not None:
            qpixmap = self.pil_image_to_qpixmap(frame)
            scaled_pixmap = qpixmap.scaledToWidth(400)
            self.preview_label.setPixmap(scaled_pixmap)

    def pil_image_to_qpixmap(self, pil_image):
        if pil_image.mode == 'RGBA':
            rgb_image = pil_image.convert('RGB')
        else:
            rgb_image = pil_image
        
        data = rgb_image.tobytes('raw', 'RGB')
        qimage = QImage(data, rgb_image.width, rgb_image.height, QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)

    def set_background(self, file_path: str):
        if not file_path or not os.path.exists(file_path):
            return
        
        self.background_type = self.determine_background_type(file_path)
        
        if self.background_type == 'image':
            self.background_image = Image.open(file_path)
            self.background_image = self.background_image.resize(
                (self.device_width, self.device_height),
                Image.Resampling.LANCZOS
            )
        elif self.background_type == 'video':
            self.background_image = file_path
        
        self.display_generator = None
        self.update_preview_frame()

    def set_foreground(self, file_path: str):
        if not file_path or not os.path.exists(file_path):
            self.foreground_image = None
            self.display_generator = None
            self.update_preview_frame()
            return
        
        self.foreground_image = Image.open(file_path)
        self.display_generator = None
        self.update_preview_frame()

    def set_foreground_opacity(self, opacity: float):
        self.foreground_opacity = max(0.0, min(1.0, opacity))
        self.display_generator = None
        self.update_preview_frame()

    def set_rotation(self, rotation: int):
        self.rotation = rotation % 360
        self.display_generator = None
        self.update_preview_frame()

    def clear_background(self, backgrounds_dir: str):
        self.background_image = Image.new('RGB', (self.device_width, self.device_height), color='white')
        self.background_type = 'color'
        self.display_generator = None
        self.update_preview_frame()

    def clear_foreground(self):
        self.foreground_image = None
        self.display_generator = None
        self.update_preview_frame()

    def clear_all(self, backgrounds_dir: str):
        self.clear_background(backgrounds_dir)
        self.clear_foreground()

    def cleanup(self):
        if self.display_generator is not None:
            if hasattr(self.display_generator, 'cleanup'):
                self.display_generator.cleanup()
        self.background_image = None
        self.foreground_image = None
        self.display_generator = None