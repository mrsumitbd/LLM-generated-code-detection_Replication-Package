import os
from pathlib import Path
from typing import Optional

from PIL import Image, ImageEnhance
from PIL.ImageQt import ImageQt

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class PreviewManager:
    """Manages display generation and frame updates for preview"""

    def __init__(self, config, preview_label: QLabel, text_style):
        """
        :param config: arbitrary configuration dictionary
        :param preview_label: QLabel where the preview will be shown
        :param text_style: unused in this implementation but kept for API compatibility
        """
        self.config = config
        self.preview_label = preview_label
        self.text_style = text_style

        # Device dimensions
        self.device_width: int = 0
        self.device_height: int = 0

        # Images
        self._background: Optional[Image.Image] = None
        self._foreground: Optional[Image.Image] = None

        # Foreground properties
        self._foreground_opacity: float = 1.0
        self._rotation: int = 0

        # Display generator function
        self._display_generator = self.create_display_generator()

    # ------------------------------------------------------------------
    # Device dimension handling
    # ------------------------------------------------------------------
    def set_device_dimensions(self, width: int, height: int):
        """Set the target device width and height for the preview."""
        self.device_width = width
        self.device_height = height
        # Resize background to fit device if already loaded
        if self._background:
            self._background = self._background.resize((width, height), Image.ANTIALIAS)

    # ------------------------------------------------------------------
    # Background handling
    # ------------------------------------------------------------------
    def initialize_default_background(self, backgrounds_dir: str):
        """Load the first image found in the backgrounds directory as default."""
        dir_path = Path(backgrounds_dir)
        if not dir_path.is_dir():
            raise FileNotFoundError(f"Backgrounds directory not found: {backgrounds_dir}")

        for file in dir_path.iterdir():
            if file.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".gif"}:
                self.set_background(str(file))
                return
        # If no image found, create a blank background
        self._background = Image.new("RGBA", (self.device_width, self.device_height), (0, 0, 0, 255))

    def determine_background_type(self, file_path):
        """Return the file extension type of the background image."""
        return Path(file_path).suffix.lower()

    def set_background(self, file_path: str):
        """Load a background image from file."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Background file not found: {file_path}")
        img = Image.open(file_path).convert("RGBA")
        if self.device_width and self.device_height:
            img = img.resize((self.device_width, self.device_height), Image.ANTIALIAS)
        self._background = img
        self.update_preview_frame()

    def clear_background(self, backgrounds_dir: str):
        """Clear background and optionally reset to default."""
        self._background = None
        self.initialize_default_background(backgrounds_dir)
        self.update_preview_frame()

    # ------------------------------------------------------------------
    # Foreground handling
    # ------------------------------------------------------------------
    def set_foreground(self, file_path: str):
        """Load a foreground image from file."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Foreground file not found: {file_path}")
        img = Image.open(file_path).convert("RGBA")
        self._foreground = img
        self.update_preview_frame()

    def set_foreground_opacity(self, opacity: float):
        """Set the opacity of the foreground image (0.0 to 1.0)."""
        if not (0.0 <= opacity <= 1.0):
            raise ValueError("Opacity must be between 0.0 and 1.0")
        self._foreground_opacity = opacity
        self.update_preview_frame()

    def set_rotation(self, rotation: int):
        """Set rotation angle for the foreground image."""
        self._rotation = rotation % 360
        self.update_preview_frame()

    def clear_foreground(self):
        """Remove the foreground image."""
        self._foreground = None
        self.update_preview_frame()

    # ------------------------------------------------------------------
    # Display generation
    # ------------------------------------------------------------------
    def create_display_generator(self):
        """Return a function that composites background and foreground."""
        def generator() -> Image.Image:
            if self._background is None:
                # Create a blank background if none set
                bg = Image.new("RGBA", (self.device_width, self.device_height), (0, 0, 0, 255))
            else:
                bg = self._background.copy()

            if self._foreground:
                fg = self._foreground.copy()
                # Apply rotation
                if self._rotation != 0:
                    fg = fg.rotate(self._rotation, expand=True, resample=Image.BICUBIC)
                # Apply opacity
                if self._foreground_opacity < 1.0:
                    alpha = fg.split()[-1]
                    alpha = ImageEnhance.Brightness(alpha).enhance(self._foreground_opacity)
                    fg.putalpha(alpha)
                # Composite onto background
                fg_w, fg_h = fg.size
                bg_w, bg_h = bg.size
                # Center the foreground
                pos = ((bg_w - fg_w) // 2, (bg_h - fg_h) // 2)
                bg.paste(fg, pos, fg)
            return bg
        return generator

    def update_preview_frame(self):
        """Generate the composite image and display it in the QLabel."""
        if not self.preview_label:
            return
        composite = self._display_generator()
        pixmap = self.pil_image_to_qpixmap(composite)
        self.preview_label.setPixmap(pixmap)

    # ------------------------------------------------------------------
    # Utility conversion
    # ------------------------------------------------------------------
    def pil_image_to_qpixmap(self, pil_image):
        """Convert a PIL Image to QPixmap."""
        if pil_image.mode != "RGBA":
            pil_image = pil_image.convert("RGBA")
        qt_image = ImageQt(pil_image)
        return QPixmap.fromImage(qt_image)

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------
    def clear_all(self, backgrounds_dir: str):
        """Clear both background and foreground, resetting to default background."""
        self.clear_foreground()
        self.clear_background(backgrounds_dir)

    def cleanup(self):
        """Release resources."""
        self._background = None
        self._foreground = None
        self.preview_label.clear()