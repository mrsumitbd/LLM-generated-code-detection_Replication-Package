import anthropic
import json
import time
from datetime import datetime, timedelta


class TimerService:
    """
    倒计时器服务，管理所有倒计时任务.
    """

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.timers = {}
        self.timer_counter = 0

    def create_timer(self, duration_seconds: int, name: str = None) -> str:
        """创建一个新的倒计时器"""
        self.timer_counter += 1
        timer_id = f"timer_{self.timer_counter}"
        
        if name is None:
            name = f"Timer {self.timer_counter}"
        
        self.timers[timer_id] = {
            "name": name,
            "duration": duration_seconds,
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(seconds=duration_seconds),
            "paused": False,
            "pause_time": None,
            "remaining": duration_seconds
        }
        
        return timer_id

    def get_timer_status(self, timer_id: str) -> dict:
        """获取倒计时器的状态"""
        if timer_id not in self.timers:
            return {"error": f"Timer {timer_id} not found"}
        
        timer = self.timers[timer_id]
        
        if timer["paused"]:
            remaining = timer["remaining"]
        else:
            elapsed = (datetime.now() - timer["start_time"]).total_seconds()
            remaining = max(0, timer["duration"] - elapsed)
        
        return {
            "timer_id": timer_id,
            "name": timer["name"],
            "duration": timer["duration"],
            "remaining": remaining,
            "paused": timer["paused"],
            "finished": remaining == 0
        }

    def pause_timer(self, timer_id: str) -> dict:
        """暂停倒计时器"""
        if timer_id not in self.timers:
            return {"error": f"Timer {timer_id} not found"}
        
        timer = self.timers[timer_id]
        if not timer["paused"]:
            elapsed = (datetime.now() - timer["start_time"]).total_seconds()
            timer["remaining"] = max(0, timer["duration"] - elapsed)
            timer["paused"] = True
            timer["pause_time"] = datetime.now()
        
        return {"status": "paused", "timer_id": timer_id, "remaining": timer["remaining"]}

    def resume_timer(self, timer_id: str) -> dict:
        """恢复倒计时器"""
        if timer_id not in self.timers:
            return {"error": f"Timer {timer_id} not found"}
        
        timer = self.timers[timer_id]
        if timer["paused"]:
            timer["paused"] = False
            timer["start_time"] = datetime.now() - timedelta(seconds=timer["duration"] - timer["remaining"])
            timer["end_time"] = datetime.now() + timedelta(seconds=timer["remaining"])
        
        return {"status": "resumed", "timer_id": timer_id}

    def cancel_timer(self, timer_id: str) -> dict:
        """取消倒计时器"""
        if timer_id not in self.timers:
            return {"error": f"Timer {timer_id} not found"}
        
        del self.timers[timer_id]
        return {"status": "cancelled", "timer_id": timer_id}

    def list_timers(self) -> list:
        """列出所有倒计时器"""
        timers_list = []
        for timer_id in self.timers:
            status = self.get_timer_status(timer_id)
            timers_list.append(status)
        return timers_list

    def process_tool_call(self, tool_name: str, tool_input: dict) -> str:
        """处理工具调用"""
        if tool_name == "create_timer":
            result = self.create_timer(
                duration_seconds=tool_input.get("duration_seconds", 60),
                name=tool_input.get("name")
            )
            return json.dumps({"timer_id": result})
        elif tool_name == "get_timer_status":
            result = self.get_timer_status(tool_input.get("timer_id"))
            return json.dumps(result)
        elif tool_name == "pause_timer":
            result = self.pause_timer(tool_input.get("timer_id"))
            return json.dumps(result)
        elif tool_name == "resume_timer":
            result = self.resume_timer(tool_input.get("timer_id"))
            return json.dumps(result)
        elif tool_name == "cancel_timer":
            result = self.cancel_timer(tool_input.get("timer_id"))
            return json.dumps(result)
        elif tool_name == "list_timers":
            result = self.list_timers()
            return json.dumps(result)
        else:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})

    def chat(self, user_message: str) -> str:
        """与Claude进行对话，处理倒计时器相关的请求"""
        tools = [
            {
                "name": "create_timer",
                "description": "创建一个新的倒计时器",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "duration_seconds": {
                            "type": "integer",
                            "description": "倒计时的秒数"
                        },
                        "name": {
                            "type": "string",
                            "description": "倒计时器的名称（可选）"
                        }
                    },
                    "required": ["duration_seconds"]
                }
            },
            {
                "name": "get_timer_status",
                "description": "获取倒计时器的当前状态",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "timer_id": {
                            "type": "string",
                            "description": "倒计时器的ID"
                        }
                    },
                    "required": ["timer_id"]
                }
            },
            {
                "name": "pause_timer",
                "description": "暂停一个倒计时器",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "timer_id": {
                            "type": "string",
                            "description": "倒计时器的ID"
                        }
                    },
                    "required": ["timer_id"]
                }
            },
            {
                "name": "resume_timer",
                "description": "恢复一个暂停的倒计时器",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "timer_id": {
                            "type": "string",
                            "description": "倒计时器的ID"
                        }
                    },
                    "required": ["timer_id"]
                }
            },
            {
                "name": "cancel_timer",
                "description": "取消一个倒计时器",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "timer_id": {
                            "type": "string",
                            "description": "倒计时器的ID"
                        }
                    },
                    "required": ["timer_id"]
                }
            },
            {
                "name": "list_timers",
                "description": "列出所有活跃的倒计时器",
                "input_schema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]

        messages = [
            {"role": "user", "content": user_message}
        ]

        while True:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                tools=tools,
                messages=messages
            )

            if response.stop_reason == "end_turn":
                for block in response.content:
                    if hasattr(block, 'text'):
                        return block.text
                return "No response generated"

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        tool_result = self.process_tool_call(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": tool_result
                        })

                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})
            else:
                break

        return "Unexpected response"


if __name__ == "__main__":
    service = TimerService()
    
    print("=== 倒计时器服务演示 ===\n")
    
    response = service.chat("请为我创建一个30秒的倒计时器，名字叫'工作计时'")
    print(f"Claude: {response}\n")
    
    response = service.chat("现在有哪些倒计时器在运行？")
    print(f"Claude: {response}\n")
    
    response = service.chat("请暂停timer_1")
    print(f"Claude: {response}\n")
    
    response = service.chat("timer_1现在的状态是什么？")
    print(f"Claude: {response}\n")
    
    response = service.chat("请恢复timer_1")
    print(f"Claude: {response}\n")
    
    response = service.chat("创建一个5秒的倒计时器用于提醒")
    print(f"Claude: {response}\n")
    
    response = service.chat("列出所有倒计时器")
    print(f"Claude: {response}\n")