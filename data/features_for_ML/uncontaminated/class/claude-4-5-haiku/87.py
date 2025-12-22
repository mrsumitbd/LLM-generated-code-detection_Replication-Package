import asyncio
import anthropic
from typing import Optional


class AsyncTask:
    """异步任务基类"""

    def __init__(self, task_name: str | None = None, wait_before_start: int = 0, run_interval: int = 0):
        self.task_name = task_name or self.__class__.__name__
        self.wait_before_start = wait_before_start
        self.run_interval = run_interval
        self._stop_event = asyncio.Event()
        self._client = anthropic.Anthropic()

    async def run(self):
        """运行异步任务"""
        if self.wait_before_start > 0:
            await asyncio.sleep(self.wait_before_start)

        while not self._stop_event.is_set():
            try:
                await self.execute()
            except Exception as e:
                print(f"Error in task {self.task_name}: {e}")

            if self.run_interval > 0:
                try:
                    await asyncio.wait_for(self._stop_event.wait(), timeout=self.run_interval)
                    break
                except asyncio.TimeoutError:
                    continue
            else:
                break

    async def execute(self):
        """执行任务的具体逻辑，子类应该重写此方法"""
        pass

    def stop(self):
        """停止任务"""
        self._stop_event.set()

    async def call_claude(self, prompt: str, model: str = "claude-3-5-sonnet-20241022") -> str:
        """调用Claude API"""
        message = self._client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text


class DemoTask(AsyncTask):
    """演示任务"""

    async def execute(self):
        """执行演示任务"""
        print(f"Running task: {self.task_name}")
        response = await self.call_claude("What is 2+2?")
        print(f"Claude response: {response}")


async def main():
    """主函数"""
    task = DemoTask(task_name="demo_task", wait_before_start=0, run_interval=0)
    await task.run()


if __name__ == "__main__":
    asyncio.run(main())