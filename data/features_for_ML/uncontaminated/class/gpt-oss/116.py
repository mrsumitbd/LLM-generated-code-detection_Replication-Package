import sys
from typing import Any, Dict, Optional

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
except Exception:
    webdriver = None  # Selenium not available


class Driver:
    def __init__(self, browser_config: Optional[Dict[str, Any]] = None, *args, **kwargs):
        self._driver: Optional[Any] = None
        if webdriver is None:
            return
        config = browser_config or {}
        browser = config.get("browser", "chrome").lower()
        options = config.get("options", {})
        try:
            if browser == "chrome":
                chrome_options = ChromeOptions()
                for opt, val in options.items():
                    if isinstance(val, bool):
                        if val:
                            chrome_options.add_argument(opt)
                    else:
                        chrome_options.add_argument(f"{opt}={val}")
                self._driver = webdriver.Chrome(
                    service=ChromeService(), options=chrome_options, *args, **kwargs
                )
            elif browser == "firefox":
                firefox_options = FirefoxOptions()
                for opt, val in options.items():
                    if isinstance(val, bool):
                        if val:
                            firefox_options.add_argument(opt)
                    else:
                        firefox_options.add_argument(f"{opt}={val}")
                self._driver = webdriver.Firefox(
                    service=FirefoxService(), options=firefox_options, *args, **kwargs
                )
            else:
                raise ValueError(f"Unsupported browser: {browser}")
        except Exception:
            self._driver = None

    def is_closed(self) -> bool:
        if self._driver is None:
            return True
        try:
            return self._driver.session_id is None
        except Exception:
            return True

    def get_context(self) -> Optional[str]:
        if self._driver is None:
            return None
        try:
            return self._driver.current_window_handle
        except Exception:
            return None

    def get_page(self) -> Optional[str]:
        if self._driver is None:
            return None
        try:
            return self._driver.page_source
        except Exception:
            return None

    def close(self) -> None:
        if self._driver is not None:
            try:
                self._driver.quit()
            finally:
                self._driver = None