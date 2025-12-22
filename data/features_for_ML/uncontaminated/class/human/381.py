import asyncio
import contextvars
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional, List, Union

class PromptContext:
    def __init__(self):
        self._context_prompts: Dict[str, Dict[str, "Prompt"]] = {}
        # 使用contextvars创建协程上下文变量
        self._current_context_var = contextvars.ContextVar("current_context", default=None)
        self._context_lock = asyncio.Lock()  # 保留锁用于其他操作

    @property
    def _current_context(self) -> Optional[str]:
        """获取当前协程的上下文ID"""
        return self._current_context_var.get()

    @_current_context.setter
    def _current_context(self, value: Optional[str]):
        """设置当前协程的上下文ID"""
        self._current_context_var.set(value)

    @asynccontextmanager
    async def async_scope(self, context_id: Optional[str] = None):
        # sourcery skip: hoist-statement-from-if, use-contextlib-suppress
        """创建一个异步的临时提示模板作用域"""
        # 保存当前上下文并设置新上下文
        if context_id is not None:
            try:
                # 添加超时保护，避免长时间等待锁
                await asyncio.wait_for(self._context_lock.acquire(), timeout=5.0)
                try:
                    if context_id not in self._context_prompts:
                        self._context_prompts[context_id] = {}
                finally:
                    self._context_lock.release()
            except asyncio.TimeoutError:
                logger.warning(f"获取上下文锁超时，context_id: {context_id}")
                # 超时时直接进入，不设置上下文
                context_id = None

            # 保存当前协程的上下文值，不影响其他协程
            previous_context = self._current_context
            # 设置当前协程的新上下文
            token = self._current_context_var.set(context_id) if context_id else None
        else:
            # 如果没有提供新上下文，保持当前上下文不变
            previous_context = self._current_context
            token = None

        try:
            yield self
        finally:
            # 恢复之前的上下文，添加异常保护
            if context_id is not None and token is not None:
                try:
                    self._current_context_var.reset(token)
                except Exception as e:
                    logger.warning(f"恢复上下文时出错: {e}")
                    # 如果reset失败，尝试直接设置
                    try:
                        self._current_context = previous_context
                    except Exception:
                        pass  # 静默忽略恢复失败

    async def get_prompt_async(self, name: str) -> Optional["Prompt"]:
        """异步获取当前作用域中的提示模板"""
        async with self._context_lock:
            current_context = self._current_context
            logger.debug(f"获取提示词: {name} 当前上下文: {current_context}")
            if (
                current_context
                and current_context in self._context_prompts
                and name in self._context_prompts[current_context]
            ):
                return self._context_prompts[current_context][name]
            return None

    async def register_async(self, prompt: "Prompt", context_id: Optional[str] = None) -> None:
        """异步注册提示模板到指定作用域"""
        async with self._context_lock:
            if target_context := context_id or self._current_context:
                self._context_prompts.setdefault(target_context, {})[prompt.name] = prompt