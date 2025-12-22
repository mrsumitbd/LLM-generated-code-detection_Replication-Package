import os
from typing import Tuple

import pyautogui


class WindowOperationsMixin:
    """
    Mixin providing window region retrieval and menu item interaction
    using PyAutoGUI. The mixin expects that menu item images are
    available as PNG files named after the menu text (e.g. "File.png").
    """

    def get_window_region(self, window: pyautogui.Window) -> Tuple[int, int, int, int]:
        """
        Return the bounding box of the given window as a tuple:
        (left, top, width, height).

        Parameters
        ----------
        window : pyautogui.Window
            The window object to query.

        Returns
        -------
        Tuple[int, int, int, int]
            The window's left, top, width, and height.
        """
        return window.left, window.top, window.width, window.height

    def find_and_click_menu_item(self, menu_text: str) -> bool:
        """
        Search the screen for an image file named after the menu text
        (e.g. "File.png") and click its center if found.

        Parameters
        ----------
        menu_text : str
            The text of the menu item to locate. An image file named
            "<menu_text>.png" must exist in the current working directory.

        Returns
        -------
        bool
            True if the menu item was found and clicked, False otherwise.
        """
        # Build the expected image file name
        image_name = f"{menu_text}.png"

        # Verify the image file exists
        if not os.path.isfile(image_name):
            return False

        # Attempt to locate the image on screen
        location = pyautogui.locateOnScreen(image_name, confidence=0.8)
        if location is None:
            return False

        # Click the center of the located region
        center = pyautogui.center(location)
        pyautogui.click(center)
        return True