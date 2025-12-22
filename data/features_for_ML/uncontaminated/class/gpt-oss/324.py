from typing import List, Tuple, Any


class ChatRoom:
    """
    群聊信息模型。
    用于描述微信群聊的基本属性和成员解析。
    """

    def __init__(self, room_id: Any, name: str, member_list_str: str | None):
        self.room_id = room_id
        self.name = name
        self.member_list_str = member_list_str or ""

    @classmethod
    def from_db_row(cls, row: Tuple[Any, ...]) -> "ChatRoom":
        """
        根据数据库查询结果行创建 ChatRoom 实例。
        预期 row 的顺序为 (room_id, name, member_list_str)。
        """
        if len(row) < 3:
            raise ValueError("DB row must contain at least 3 elements: room_id, name, member_list_str")
        room_id, name, member_list_str = row[0], row[1], row[2]
        return cls(room_id, name, member_list_str)

    @property
    def parsed_member_list(self) -> List[str]:
        """
        将 member_list_str 按逗号分隔并去除空白，返回成员列表。
        """
        if not self.member_list_str:
            return []
        return [m.strip() for m in self.member_list_str.split(",") if m.strip()]