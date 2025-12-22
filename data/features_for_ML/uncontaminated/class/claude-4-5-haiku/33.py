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
        """
        将Message对象转换为FakeMessage字典格式
        """
        self.local_id = getattr(message, 'local_id', None)
        self.local_type = getattr(message, 'local_type', None)
        self.message_content = getattr(message, 'message_content', None)
        self.username = getattr(message, 'username', None)
        self.nickname = getattr(message, 'nickname', None)
        self.at_list = getattr(message, 'at_list', [])
        self.is_chatroom = getattr(message, 'is_chatroom', False)
        self.create_time = getattr(message, 'create_time', None)
        self.quote_msg = getattr(message, 'quote_msg', None)
        self.thumb = getattr(message, 'thumb', None)
        self.image = getattr(message, 'image', None)
        self.video = getattr(message, 'video', None)
        self.file = getattr(message, 'file', None)

        return self.to_dict()

    def to_dict(self) -> dict:
        """
        将FakeMessage对象转换为字典
        """
        return {
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
            'file': self.file,
        }

    def __repr__(self) -> str:
        return f"FakeMessage({self.to_dict()})"