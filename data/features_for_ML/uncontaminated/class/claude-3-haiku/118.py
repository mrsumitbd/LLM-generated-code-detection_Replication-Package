import pyautogui
from typing import Tuple

class WindowOperationsMixin:
    def get_window_region(self, window: pyautogui.Window) -> Tuple[int, int, int, int]:
        x, y, width, height = window.left, window.top, window.width, window.height
        return x, y, width, height

    def find_and_click_menu_item(self, menu_text: str) -> bool:
        try:
            menu_item_location = pyautogui.locateOnScreen(f"{menu_text}.png", confidence=0.8)
            if menu_item_location:
                x, y = pyautogui.center(menu_item_location)
                pyautogui.click(x, y)
                return True
            else:
                return False
        except (pyautogui.ImageNotFoundException, pyautogui.PyAutoGUIException):
            return False