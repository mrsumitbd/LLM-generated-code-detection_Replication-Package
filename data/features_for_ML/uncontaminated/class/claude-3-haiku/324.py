from typing import List

class ChatRoom:
    """
    群聊信息模型。
    用于描述微信群聊的基本属性和成员解析。
    """

    def __init__(self, room_id: str, room_name: str, member_list: str):
        self._room_id = room_id
        self._room_name = room_name
        self._member_list = member_list

    @classmethod
    def from_db_row(cls, row: tuple) -> "ChatRoom":
        room_id, room_name, member_list = row
        return cls(room_id, room_name, member_list)

    @property
    def parsed_member_list(self) -> List[str]:
        return self._member_list.split(',')

    @property
    def room_id(self) -> str:
        return self._room_id

    @property
    def room_name(self) -> str:
        return self._room_name