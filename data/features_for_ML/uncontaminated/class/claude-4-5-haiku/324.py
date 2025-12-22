class ChatRoom:
    """
    群聊信息模型。
    用于描述微信群聊的基本属性和成员解析。
    """

    def __init__(self, chat_room_id: str, member_list: str, nick_name: str = "", display_name: str = ""):
        self.chat_room_id = chat_room_id
        self.member_list = member_list
        self.nick_name = nick_name
        self.display_name = display_name

    @classmethod
    def from_db_row(cls, row: tuple) -> "ChatRoom":
        """从数据库行创建ChatRoom实例"""
        if len(row) >= 4:
            return cls(
                chat_room_id=row[0],
                member_list=row[1],
                nick_name=row[2],
                display_name=row[3]
            )
        elif len(row) >= 2:
            return cls(
                chat_room_id=row[0],
                member_list=row[1]
            )
        else:
            raise ValueError("Invalid row data for ChatRoom")

    @property
    def parsed_member_list(self) -> List[str]:
        """解析成员列表字符串为列表"""
        if not self.member_list:
            return []
        
        # 处理常见的分隔符：逗号、分号、换行符等
        members = []
        separators = [',', ';', '\n', '|', '、']
        
        member_str = self.member_list.strip()
        
        for separator in separators:
            if separator in member_str:
                members = [m.strip() for m in member_str.split(separator) if m.strip()]
                break
        
        if not members:
            members = [member_str] if member_str else []
        
        return members