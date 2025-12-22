import re
from datetime import datetime
from typing import List

class XHSDataCollector:
    """小红书数据采集器"""

    def __init__(self, browser_manager: "IBrowserManager"):
        """
        初始化数据采集器，保存浏览器管理器实例。

        :param browser_manager: 用于控制浏览器的管理器实例
        """
        self.browser_manager = browser_manager

    def get_supported_data_types(self) -> List[str]:
        """
        返回小红书支持的数据类型列表。

        :return: 支持的数据类型列表
        """
        return ["posts", "comments", "likes", "shares", "profile"]

    def validate_date_format(self, date: str) -> bool:
        """
        验证日期字符串是否符合 YYYY-MM-DD 格式。

        :param date: 待验证的日期字符串
        :return: 如果格式正确返回 True，否则返回 False
        """
        if not isinstance(date, str):
            return False
        # 先用正则快速过滤
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            return False
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False