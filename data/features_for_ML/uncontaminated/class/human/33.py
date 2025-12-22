from typing import Any, List, Optional, Union

class FakeMessage:
    """
    自定义的消息类型，这个是双向的，和外部交互用这个类型
    用于在消息处理过程中，将消息转换为自定义的消息类型
    用户的消息，初步设计为 文本，图片，视频，文件，其他，表情等归属于文本
    其他消息类型，如语音，视频，文件，位置，名片，转账，红包，系统消息，撤回消息等，归属于其他
    不同的操作，感觉RPA也是可以操作的
    发送成功之后，会有一条真实的消息生成，可以作为客户端的反馈
    这里是一条简化的消息，只需要能够被RPA处理就可以了，微信不能批量操作，因此每条消息的附件是唯一的
    生成字段注释
    local_id: 本地消息ID
    local_type: 本地消息类型
    message_content: 消息内容
    username: 用户名, 如果是群聊，这个就是群
    nickname: 昵称
    at_list: 被@的人列表
    is_chatroom: 是否为群聊
    create_time: 消息创建时间
    quote_msg: 引用消息
    thumb: 缩略图
    image: 图片
    video: 视频
    file: 文件
    """

    local_id: int
    local_type: int
    message_content: str
    username: str
    nickname: str
    at_list: List[str]
    is_chatroom: bool
    create_time: int
    quote_msg: Optional[str] = None
    thumb: Optional[bytes] = None
    image: Optional[bytes] = None
    video: Optional[bytes] = None
    file: Optional[bytes] = None

    def from_message(self, message: Message) -> dict:
        return {
            "local_id": message.local_id,
            "local_type": message.local_type,
            "message_content": message.message_content,
            "username": message.username,
        }