from IBrowserManager import IBrowserManager

class CompatibilityAdapter:
    """
    兼容性适配器
    
    为了保持向后兼容，提供与原XHSClient相同的接口
    """

    def __init__(self, browser_manager: IBrowserManager):
        self.browser_manager = browser_manager