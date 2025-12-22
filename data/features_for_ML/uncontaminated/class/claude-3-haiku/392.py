class CompatibilityAdapter:
    """
    兼容性适配器
    
    为了保持向后兼容，提供与原XHSClient相同的接口
    """

    def __init__(self, browser_manager: IBrowserManager):
        self._browser_manager = browser_manager

    def login(self, username: str, password: str) -> bool:
        return self._browser_manager.login(username, password)

    def logout(self) -> bool:
        return self._browser_manager.logout()

    def get_user_info(self) -> dict:
        return self._browser_manager.get_user_info()

    def get_feed(self, max_count: int = 20) -> list:
        return self._browser_manager.get_feed(max_count)

    def get_post_detail(self, post_id: str) -> dict:
        return self._browser_manager.get_post_detail(post_id)

    def comment(self, post_id: str, content: str) -> bool:
        return self._browser_manager.comment(post_id, content)

    def like(self, post_id: str) -> bool:
        return self._browser_manager.like(post_id)

    def unlike(self, post_id: str) -> bool:
        return self._browser_manager.unlike(post_id)

    def upload_post(self, content: str, images: list) -> bool:
        return self._browser_manager.upload_post(content, images)