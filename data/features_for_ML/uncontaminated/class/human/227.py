import asyncio
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import json

class TimerService:
    """
    倒计时器服务，管理所有倒计时任务.
    """

    def __init__(self):
        # 使用字典存储活动的计时器，键是 timer_id，值是 TimerTask 对象
        self._timers: Dict[int, "TimerTask"] = {}
        self._next_timer_id = 0
        # 使用锁来保护对 _timers 和 _next_timer_id 的访问，确保线程安全
        self._lock = asyncio.Lock()
        self.DEFAULT_DELAY = 5  # 默认延迟秒数

    async def start_countdown(
        self, command: str, delay: int = None, description: str = ""
    ) -> Dict[str, Any]:
        """启动一个倒计时任务.

        Args:
            command: 要执行的MCP工具调用 (JSON格式字符串，包含name和arguments字段)
            delay: 延迟时间（秒），默认为5秒
            description: 任务描述

        Returns:
            Dict[str, Any]: 包含任务信息的字典
        """
        if delay is None:
            delay = self.DEFAULT_DELAY

        # 验证延迟时间
        try:
            delay = int(delay)
            if delay <= 0:
                logger.warning(
                    f"提供的延迟时间 {delay} 无效，使用默认值 {self.DEFAULT_DELAY} 秒"
                )
                delay = self.DEFAULT_DELAY
        except (ValueError, TypeError):
            logger.warning(
                f"提供的延迟时间 '{delay}' 无效，使用默认值 {self.DEFAULT_DELAY} 秒"
            )
            delay = self.DEFAULT_DELAY

        # 验证命令格式
        try:
            json.loads(command)
        except json.JSONDecodeError:
            logger.error(f"启动倒计时失败：命令格式错误，无法解析JSON: {command}")
            return {
                "success": False,
                "message": f"命令格式错误，无法解析JSON: {command}",
            }

        # 获取当前事件循环
        loop = asyncio.get_running_loop()

        async with self._lock:
            timer_id = self._next_timer_id
            self._next_timer_id += 1

            # 创建倒计时任务
            timer_task = TimerTask(
                timer_id=timer_id,
                command=command,
                delay=delay,
                description=description,
                service=self,
            )

            # 创建异步任务
            task = loop.create_task(timer_task.run())
            timer_task.task = task

            self._timers[timer_id] = timer_task

        logger.info(f"启动倒计时 {timer_id}，将在 {delay} 秒后执行命令: {command}")

        return {
            "success": True,
            "message": f"倒计时 {timer_id} 已启动，将在 {delay} 秒后执行",
            "timer_id": timer_id,
            "delay": delay,
            "command": command,
            "description": description,
            "start_time": datetime.now().isoformat(),
            "estimated_execution_time": (
                datetime.now() + timedelta(seconds=delay)
            ).isoformat(),
        }

    async def cancel_countdown(self, timer_id: int) -> Dict[str, Any]:
        """取消指定的倒计时任务.

        Args:
            timer_id: 要取消的计时器ID

        Returns:
            Dict[str, Any]: 取消结果
        """
        try:
            timer_id = int(timer_id)
        except (ValueError, TypeError):
            logger.error(f"取消倒计时失败：无效的 timer_id {timer_id}")
            return {"success": False, "message": f"无效的 timer_id: {timer_id}"}

        async with self._lock:
            if timer_id in self._timers:
                timer_task = self._timers.pop(timer_id)
                if timer_task.task:
                    timer_task.task.cancel()

                logger.info(f"倒计时 {timer_id} 已成功取消")
                return {
                    "success": True,
                    "message": f"倒计时 {timer_id} 已取消",
                    "timer_id": timer_id,
                    "cancelled_at": datetime.now().isoformat(),
                }
            else:
                logger.warning(f"尝试取消不存在或已完成的倒计时 {timer_id}")
                return {
                    "success": False,
                    "message": f"找不到ID为 {timer_id} 的活动倒计时",
                    "timer_id": timer_id,
                }

    async def get_active_timers(self) -> Dict[str, Any]:
        """获取所有活动的倒计时任务状态.

        Returns:
            Dict[str, Any]: 活动计时器列表
        """
        async with self._lock:
            active_timers = []
            current_time = datetime.now()

            for timer_id, timer_task in self._timers.items():
                remaining_time = timer_task.get_remaining_time()
                if remaining_time > 0:
                    active_timers.append(
                        {
                            "timer_id": timer_id,
                            "command": timer_task.command,
                            "description": timer_task.description,
                            "delay": timer_task.delay,
                            "remaining_seconds": remaining_time,
                            "start_time": timer_task.start_time.isoformat(),
                            "estimated_execution_time": timer_task.execution_time.isoformat(),
                            "progress": timer_task.get_progress(),
                        }
                    )

            return {
                "success": True,
                "total_active_timers": len(active_timers),
                "timers": active_timers,
                "current_time": current_time.isoformat(),
            }

    async def cleanup_timer(self, timer_id: int):
        """
        从管理器中移除已完成的计时器.
        """
        async with self._lock:
            if timer_id in self._timers:
                del self._timers[timer_id]
                logger.debug(f"已清理完成的倒计时 {timer_id}")

    async def cleanup_all(self):
        """
        清理所有倒计时任务（应用关闭时调用）
        """
        logger.info("正在清理所有倒计时任务...")
        async with self._lock:
            active_timer_ids = list(self._timers.keys())
            for timer_id in active_timer_ids:
                if timer_id in self._timers:
                    timer_task = self._timers.pop(timer_id)
                    if timer_task.task:
                        timer_task.task.cancel()
                    logger.info(f"已取消倒计时任务 {timer_id}")
        logger.info("倒计时任务清理完成")