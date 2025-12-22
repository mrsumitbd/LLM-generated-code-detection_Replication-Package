from typing import List

class FakeMessage:
    def __init__(self):
        self.local_id = None
        self.local_type = None
        self.message_content = None
        self.username = None
        self.nickname = None
        self.at_list = []
        self.is_chatroom = False
        self.create_time = None
        self.quote_msg = None
        self.thumb = None
        self.image = None
        self.video = None
        self.file = None

    def from_message(self, message: Message) -> dict:
        fake_message = {
            'local_id': self.local_id,
            'local_type': self.local_type,
            'message_content': self.message_content,
            'username': self.username,
            'nickname': self.nickname,
            'at_list': self.at_list,
            'is_chatroom': self.is_chatroom,
            'create_time': self.create_time,
            'quote_msg': self.quote_msg,
            'thumb': self.thumb,
            'image': self.image,
            'video': self.video,
            'file': self.file
        }
        return fake_message