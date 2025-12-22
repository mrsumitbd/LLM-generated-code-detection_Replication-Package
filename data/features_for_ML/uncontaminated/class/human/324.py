import hashlib
from typing import Dict, List
from omni_bot_sdk.weixin.parser.util.protocbuf.roomdata_pb2 import ChatRoomData

class ChatRoom:
    """
    群聊信息模型。
    用于描述微信群聊的基本属性和成员解析。
    """

    id: int  # 数据库主键
    username: str  # 群聊唯一标识
    owner: str  # 群主用户名
    ext_buffer: bytes  # 扩展缓冲区（含成员信息）
    username_md5: str  # 群聊用户名MD5

    @classmethod
    def from_db_row(cls, row: tuple) -> "ChatRoom":
        """
        从数据库行数据创建ChatRoom对象。
        """
        username = row[1]
        username_md5 = hashlib.md5(username.encode()).hexdigest()
        return cls(
            id=row[0],
            username=username,
            owner=row[2],
            ext_buffer=row[3],
            username_md5=username_md5,
        )

    @property
    def parsed_member_list(self) -> List[str]:
        """
        解析群聊成员列表。
        通过解析ext_buffer中的protobuf数据，提取所有成员的wxID。
        结果缓存至实例属性，避免重复解析。
        """
        if not hasattr(self, "_parsed_member_list"):
            ext_buffer = self.ext_buffer
            if isinstance(ext_buffer, bytes):
                parsechatroom = ChatRoomData()
                parsechatroom.ParseFromString(ext_buffer)
                self._parsed_member_list = [
                    member.wxID for member in parsechatroom.members
                ]

        return self._parsed_member_list