class XHSMessages:
    """小红书相关消息常量"""

    # 登录相关
    LOGIN_SUCCESS = "登录成功"
    LOGIN_FAILED = "登录失败"
    LOGIN_TIMEOUT = "登录超时"
    LOGIN_NETWORK_ERROR = "网络错误，登录失败"

    # 发布相关
    POST_SUCCESS = "发布成功"
    POST_FAILED = "发布失败"
    POST_TIMEOUT = "发布超时"
    POST_NETWORK_ERROR = "网络错误，发布失败"

    # 评论相关
    COMMENT_SUCCESS = "评论成功"
    COMMENT_FAILED = "评论失败"
    COMMENT_TIMEOUT = "评论超时"
    COMMENT_NETWORK_ERROR = "网络错误，评论失败"

    # 点赞相关
    LIKE_SUCCESS = "点赞成功"
    LIKE_FAILED = "点赞失败"
    LIKE_TIMEOUT = "点赞超时"
    LIKE_NETWORK_ERROR = "网络错误，点赞失败"

    # 关注相关
    FOLLOW_SUCCESS = "关注成功"
    FOLLOW_FAILED = "关注失败"
    FOLLOW_TIMEOUT = "关注超时"
    FOLLOW_NETWORK_ERROR = "网络错误，关注失败"

    # 取关相关
    UNFOLLOW_SUCCESS = "取关成功"
    UNFOLLOW_FAILED = "取关失败"
    UNFOLLOW_TIMEOUT = "取关超时"
    UNFOLLOW_NETWORK_ERROR = "网络错误，取关失败"

    # 获取帖子相关
    FETCH_POSTS_SUCCESS = "获取帖子成功"
    FETCH_POSTS_FAILED = "获取帖子失败"
    FETCH_POSTS_TIMEOUT = "获取帖子超时"
    FETCH_POSTS_NETWORK_ERROR = "网络错误，获取帖子失败"

    # 获取用户信息相关
    FETCH_USER_INFO_SUCCESS = "获取用户信息成功"
    FETCH_USER_INFO_FAILED = "获取用户信息失败"
    FETCH_USER_INFO_TIMEOUT = "获取用户信息超时"
    FETCH_USER_INFO_NETWORK_ERROR = "网络错误，获取用户信息失败"

    # 通用错误
    UNKNOWN_ERROR = "未知错误"
    PERMISSION_DENIED = "权限不足"
    INVALID_TOKEN = "无效或已过期的令牌"

    # 状态码
    SUCCESS_CODE = 0
    ERROR_CODE = 1
    TIMEOUT_CODE = 2
    NETWORK_ERROR_CODE = 3
    AUTH_ERROR_CODE = 4
    PERMISSION_ERROR_CODE = 5
    UNKNOWN_ERROR_CODE = 99

    @classmethod
    def get_message(cls, code: int) -> str:
        """根据状态码返回对应的消息"""
        mapping = {
            cls.SUCCESS_CODE: cls.LOGIN_SUCCESS,
            cls.ERROR_CODE: cls.UNKNOWN_ERROR,
            cls.TIMEOUT_CODE: cls.LOGIN_TIMEOUT,
            cls.NETWORK_ERROR_CODE: cls.LOGIN_NETWORK_ERROR,
            cls.AUTH_ERROR_CODE: cls.INVALID_TOKEN,
            cls.PERMISSION_ERROR_CODE: cls.PERMISSION_DENIED,
            cls.UNKNOWN_ERROR_CODE: cls.UNKNOWN_ERROR,
        }
        return mapping.get(code, cls.UNKNOWN_ERROR)