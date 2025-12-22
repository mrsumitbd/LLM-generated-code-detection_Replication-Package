from typing import List
from browser_manager import IBrowserManager

class XHSDataCollector:
    """小红书数据采集器"""

    def __init__(self, browser_manager: IBrowserManager):
        self.browser_manager = browser_manager

    def get_supported_data_types(self) -> List[str]:
        return ["text", "image", "video"]

    def validate_date_format(self, date: str) -> bool:
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False