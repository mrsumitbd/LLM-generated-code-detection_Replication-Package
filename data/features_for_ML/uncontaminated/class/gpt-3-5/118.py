from typing import Tuple
import pyautogui

class WindowOperationsMixin:

    def get_window_region(self, window: pyautogui.Window) -> Tuple[int, int, int, int]:
        left, top, width, height = window.region
        return left, top, left + width, top + height

    def find_and_click_menu_item(self, menu_text: str) -> bool:
        menu_location = pyautogui.locateCenterOnScreen('menu.png', confidence=0.8)
        if menu_location is not None:
            pyautogui.click(menu_location)
            item_location = pyautogui.locateCenterOnScreen('item.png', confidence=0.8)
            if item_location is not None:
                pyautogui.click(item_location)
                return True
        return False