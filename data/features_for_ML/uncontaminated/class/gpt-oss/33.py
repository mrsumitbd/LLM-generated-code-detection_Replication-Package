from __future__ import annotations
from typing import Any, Dict, List, Optional, Union


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

    def from_message(self, message: Any) -> Dict[str, Any]:
        """
        将外部 Message 对象转换为自定义的字典结构。
        支持常见属性名的映射，若属性不存在则使用默认值。
        """
        def _get(attr_names: List[str], default: Any = None) -> Any:
            for name in attr_names:
                if hasattr(message, name):
                    return getattr(message, name)
            return default

        # 基础字段
        local_id = _get(["id", "local_id"])
        local_type = _get(["type", "local_type"])
        message_content = _get(["text", "content", "message"])
        username = _get(["sender", "username", "chat"])
        nickname = _get(["sender_nickname", "nickname"])
        at_list_raw = _get(["at", "at_list", "mentions"])
        is_chatroom = _get(["is_group", "is_chatroom"], False)
        create_time = _get(["timestamp", "create_time", "time"])

        # 处理 at_list
        if isinstance(at_list_raw, (list, tuple)):
            at_list = list(at_list_raw)
        elif isinstance(at_list_raw, str):
            at_list = [at_list_raw]
        else:
            at_list = []

        # 处理引用消息
        quote_raw = _get(["quote", "quote_msg", "quoted_message"])
        if quote_raw:
            if hasattr(quote_raw, "to_dict"):
                quote_msg = quote_raw.to_dict()
            else:
                quote_msg = self.from_message(quote_raw)
        else:
            quote_msg = None

        # 附件字段
        thumb = _get(["thumb", "thumbnail", "thumb_url"])
        image = _get(["image", "photo", "image_url"])
        video = _get(["video", "video_file", "video_url"])
        file = _get(["file", "document", "file_url"])

        return {
            "local_id": local_id,
            "local_type": local_type,
            "message_content": message_content,
            "username": username,
            "nickname": nickname,
            "at_list": at_list,
            "is_chatroom": bool(is_chatroom),
            "create_time": create_time,
            "quote_msg": quote_msg,
            "thumb": thumb,
            "image": image,
            "video": video,
            "file": file,
        }