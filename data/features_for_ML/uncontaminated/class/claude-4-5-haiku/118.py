class WindowOperationsMixin:

    def get_window_region(self, window: pyautogui.Window) -> Tuple[int, int, int, int]:
        """Get the region (left, top, width, height) of a window."""
        try:
            return (window.left, window.top, window.width, window.height)
        except AttributeError:
            return (0, 0, 0, 0)

    def find_and_click_menu_item(self, menu_text: str) -> bool:
        """Find and click a menu item by text."""
        try:
            import pyautogui
            from PIL import Image
            import pytesseract
            
            # Take a screenshot of the current screen
            screenshot = pyautogui.screenshot()
            
            # Use OCR to find text locations
            data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
            
            # Search for the menu text
            for i, text in enumerate(data['text']):
                if menu_text.lower() in text.lower():
                    # Get coordinates of the found text
                    x = data['left'][i] + data['width'][i] // 2
                    y = data['top'][i] + data['height'][i] // 2
                    
                    # Click on the menu item
                    pyautogui.click(x, y)
                    return True
            
            return False
        except Exception:
            return False