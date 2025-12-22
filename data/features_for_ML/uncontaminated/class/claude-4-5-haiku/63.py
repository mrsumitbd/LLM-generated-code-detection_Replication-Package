class XHSDataCollector:
    """小红书数据采集器"""

    def __init__(self, browser_manager: IBrowserManager):
        self.browser_manager = browser_manager
        self.supported_data_types = [
            "feed",
            "user_profile",
            "comments",
            "likes",
            "shares",
            "followers",
            "following",
            "search_results",
            "trending",
            "hashtags"
        ]

    def get_supported_data_types(self) -> list:
        return self.supported_data_types

    def validate_date_format(self, date: str) -> bool:
        import re
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, date):
            return False
        try:
            from datetime import datetime
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False