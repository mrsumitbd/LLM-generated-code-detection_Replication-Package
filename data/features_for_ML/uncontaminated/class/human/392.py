from typing import Optional, Dict, Any
from .models import XHSNote, XHSPublishResult
from .interfaces import IXHSClient, IBrowserManager, IDataCollector

class CompatibilityAdapter:
    """
    兼容性适配器
    
    为了保持向后兼容，提供与原XHSClient相同的接口
    """
    
    def __init__(self, browser_manager: IBrowserManager):
        self.refactored_client = RefactoredXHSClient(browser_manager)
    
    async def publish_note(self, note: XHSNote) -> XHSPublishResult:
        """兼容原publish_note接口"""
        return await self.refactored_client.publish_note(note)
    
    async def collect_creator_data(self, date: Optional[str] = None) -> Dict[str, Any]:
        """兼容原collect_creator_data接口"""
        return await self.refactored_client.collect_creator_data(date)
    
    # 添加其他需要兼容的方法... 