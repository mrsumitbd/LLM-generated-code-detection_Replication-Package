from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class IBrowserManager(Protocol):
    """Protocol for the browser manager used by the compatibility adapter."""

    def close(self) -> None: ...

    def __getattr__(self, name: str) -> Any: ...


class CompatibilityAdapter:
    """
    兼容性适配器

    为了保持向后兼容，提供与原 XHSClient 相同的接口。
    该适配器将所有未知属性和方法调用转发给内部的
    IBrowserManager 实例，从而实现对旧接口的兼容。
    """

    def __init__(self, browser_manager: IBrowserManager):
        self._browser_manager = browser_manager

    def close(self) -> None:
        """关闭底层浏览器管理器。"""
        self._browser_manager.close()

    def __enter__(self) -> "CompatibilityAdapter":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def __getattr__(self, name: str) -> Any:
        """
        任何未在本类中定义的属性或方法都会被转发到
        内部的浏览器管理器实例。
        """
        return getattr(self._browser_manager, name)

    def __repr__(self) -> str:
        return f"<CompatibilityAdapter wrapped={repr(self._browser_manager)}>"