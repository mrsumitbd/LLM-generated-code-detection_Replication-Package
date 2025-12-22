class CompatibilityAdapter:
    """
    兼容性适配器
    
    为了保持向后兼容，提供与原XHSClient相同的接口
    """

    def __init__(self, browser_manager: IBrowserManager):
        self.browser_manager = browser_manager
        self._client = None
        self._initialized = False

    def _ensure_initialized(self):
        """确保客户端已初始化"""
        if not self._initialized:
            self._client = self.browser_manager.get_client()
            self._initialized = True

    def search(self, keyword: str, page: int = 1, page_size: int = 30, sort: str = "general", note_type: int = 0):
        """搜索笔记"""
        self._ensure_initialized()
        return self._client.search(keyword, page, page_size, sort, note_type)

    def get_note_by_id(self, note_id: str):
        """根据笔记ID获取笔记详情"""
        self._ensure_initialized()
        return self._client.get_note_by_id(note_id)

    def get_user_info(self, user_id: str):
        """获取用户信息"""
        self._ensure_initialized()
        return self._client.get_user_info(user_id)

    def get_user_notes(self, user_id: str, cursor: str = "", page_size: int = 30):
        """获取用户笔记列表"""
        self._ensure_initialized()
        return self._client.get_user_notes(user_id, cursor, page_size)

    def get_user_collected(self, user_id: str, cursor: str = "", page_size: int = 30):
        """获取用户收藏列表"""
        self._ensure_initialized()
        return self._client.get_user_collected(user_id, cursor, page_size)

    def get_note_comments(self, note_id: str, cursor: str = "", page_size: int = 30):
        """获取笔记评论"""
        self._ensure_initialized()
        return self._client.get_note_comments(note_id, cursor, page_size)

    def like_note(self, note_id: str):
        """点赞笔记"""
        self._ensure_initialized()
        return self._client.like_note(note_id)

    def unlike_note(self, note_id: str):
        """取消点赞笔记"""
        self._ensure_initialized()
        return self._client.unlike_note(note_id)

    def collect_note(self, note_id: str):
        """收藏笔记"""
        self._ensure_initialized()
        return self._client.collect_note(note_id)

    def uncollect_note(self, note_id: str):
        """取消收藏笔记"""
        self._ensure_initialized()
        return self._client.uncollect_note(note_id)

    def follow_user(self, user_id: str):
        """关注用户"""
        self._ensure_initialized()
        return self._client.follow_user(user_id)

    def unfollow_user(self, user_id: str):
        """取消关注用户"""
        self._ensure_initialized()
        return self._client.unfollow_user(user_id)

    def close(self):
        """关闭浏览器"""
        if self._initialized and self._client:
            self._client.close()
        self.browser_manager.close()
        self._initialized = False
        self._client = None

    def __enter__(self):
        """上下文管理器入口"""
        self._ensure_initialized()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
        return False