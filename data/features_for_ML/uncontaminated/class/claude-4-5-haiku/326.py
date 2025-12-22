import anthropic
import json
from datetime import datetime


class UniversalMessageSender:
    """管理消息的注册、即时处理、发送和存储，并跟踪思考状态。"""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.messages = []
        self.thinking_state = None
        self.message_handlers = {}
        self.model = "claude-3-7-sonnet-20250219"

    def register_handler(self, message_type: str, handler):
        """注册消息类型的处理器"""
        self.message_handlers[message_type] = handler

    def send_message(self, content: str, message_type: str = "text", use_thinking: bool = False):
        """发送消息并获取响应"""
        self.thinking_state = "processing" if use_thinking else "idle"
        
        system_prompt = "You are a helpful assistant."
        
        if use_thinking:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=16000,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 10000
                },
                system=system_prompt,
                messages=[
                    {"role": "user", "content": content}
                ]
            )
        else:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": content}
                ]
            )
        
        # 处理响应
        result = {
            "timestamp": datetime.now().isoformat(),
            "message_type": message_type,
            "content": content,
            "response": None,
            "thinking": None,
            "thinking_state": self.thinking_state
        }
        
        for block in response.content:
            if block.type == "thinking":
                result["thinking"] = block.thinking
                self.thinking_state = "completed"
            elif block.type == "text":
                result["response"] = block.text
        
        # 存储消息
        self.messages.append(result)
        
        # 调用注册的处理器
        if message_type in self.message_handlers:
            self.message_handlers[message_type](result)
        
        return result

    def get_messages(self, message_type: str = None):
        """获取存储的消息"""
        if message_type is None:
            return self.messages
        return [msg for msg in self.messages if msg["message_type"] == message_type]

    def get_thinking_state(self):
        """获取当前思考状态"""
        return self.thinking_state

    def clear_messages(self):
        """清空消息历史"""
        self.messages = []
        self.thinking_state = None

    def process_batch_messages(self, messages_list: list, use_thinking: bool = False):
        """批量处理消息"""
        results = []
        for msg in messages_list:
            if isinstance(msg, dict):
                content = msg.get("content", "")
                msg_type = msg.get("type", "text")
            else:
                content = msg
                msg_type = "text"
            
            result = self.send_message(content, msg_type, use_thinking)
            results.append(result)
        
        return results

    def export_messages(self, format_type: str = "json"):
        """导出消息"""
        if format_type == "json":
            return json.dumps(self.messages, indent=2, ensure_ascii=False)
        elif format_type == "text":
            text_output = ""
            for msg in self.messages:
                text_output += f"[{msg['timestamp']}] Type: {msg['message_type']}\n"
                text_output += f"User: {msg['content']}\n"
                if msg['thinking']:
                    text_output += f"Thinking: {msg['thinking']}\n"
                text_output += f"Response: {msg['response']}\n"
                text_output += "-" * 50 + "\n"
            return text_output
        else:
            raise ValueError(f"Unsupported format: {format_type}")


def main():
    sender = UniversalMessageSender()
    
    # 注册一个简单的处理器
    def log_handler(message):
        print(f"[Handler] Processed message: {message['message_type']}")
    
    sender.register_handler("text", log_handler)
    
    # 发送普通消息
    print("=== 发送普通消息 ===")
    result1 = sender.send_message("你好，请介绍一下自己", "text")
    print(f"Response: {result1['response']}")
    
    # 发送带思考的消息
    print("\n=== 发送带思考的消息 ===")
    result2 = sender.send_message("2+2等于多少？请详细解释", "text", use_thinking=True)
    print(f"Response: {result2['response']}")
    if result2['thinking']:
        print(f"Thinking: {result2['thinking'][:200]}...")
    
    # 批量处理消息
    print("\n=== 批量处理消息 ===")
    batch_messages = [
        {"content": "Python是什么？", "type": "text"},
        {"content": "如何学习编程？", "type": "text"}
    ]
    batch_results = sender.process_batch_messages(batch_messages)
    print(f"Processed {len(batch_results)} messages")
    
    # 获取消息统计
    print("\n=== 消息统计 ===")
    all_messages = sender.get_messages()
    print(f"Total messages: {len(all_messages)}")
    print(f"Current thinking state: {sender.get_thinking_state()}")
    
    # 导出消息
    print("\n=== 导出消息 ===")
    json_export = sender.export_messages("json")
    print(f"JSON export length: {len(json_export)} characters")


if __name__ == "__main__":
    main()