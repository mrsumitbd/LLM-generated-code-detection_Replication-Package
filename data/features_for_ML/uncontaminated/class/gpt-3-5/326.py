class UniversalMessageSender:
    """管理消息的注册、即时处理、发送和存储，并跟踪思考状态。"""

    def __init__(self):
        self.registered_messages = []
        self.processed_messages = []
        self.sent_messages = []
        self.thoughts = {}

    def register_message(self, message):
        self.registered_messages.append(message)

    def process_message(self, message):
        self.processed_messages.append(message)

    def send_message(self, message):
        self.sent_messages.append(message)

    def track_thought(self, message, thought):
        self.thoughts[message] = thought

    def get_registered_messages(self):
        return self.registered_messages

    def get_processed_messages(self):
        return self.processed_messages

    def get_sent_messages(self):
        return self.sent_messages

    def get_thoughts(self):
        return self.thoughts