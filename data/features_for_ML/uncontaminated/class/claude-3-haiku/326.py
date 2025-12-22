class UniversalMessageSender:
    """管理消息的注册、即时处理、发送和存储，并跟踪思考状态。"""

    def __init__(self):
        self.registered_messages = {}
        self.message_queue = []
        self.thinking_state = False

    def register_message(self, message_type, message_handler):
        """注册一个新的消息类型及其处理函数。"""
        self.registered_messages[message_type] = message_handler

    def process_message(self, message):
        """立即处理给定的消息。"""
        message_type = message.get("type")
        if message_type in self.registered_messages:
            message_handler = self.registered_messages[message_type]
            message_handler(message)
        else:
            print(f"未注册的消息类型: {message_type}")

    def send_message(self, message):
        """将消息添加到队列中等待发送。"""
        self.message_queue.append(message)

    def flush_messages(self):
        """发送队列中的所有消息。"""
        while self.message_queue:
            message = self.message_queue.pop(0)
            self.process_message(message)

    def start_thinking(self):
        """开始思考状态。"""
        self.thinking_state = True

    def stop_thinking(self):
        """停止思考状态。"""
        self.thinking_state = False