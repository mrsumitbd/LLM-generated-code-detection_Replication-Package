class XHSMessages:
    """小红书相关消息常量"""
    
    # 通用消息
    SUCCESS = "操作成功"
    FAILURE = "操作失败"
    ERROR = "发生错误"
    
    # 登录相关
    LOGIN_SUCCESS = "登录成功"
    LOGIN_FAILED = "登录失败"
    LOGIN_REQUIRED = "需要登录"
    INVALID_CREDENTIALS = "用户名或密码错误"
    ACCOUNT_LOCKED = "账户已被锁定"
    
    # 内容相关
    POST_SUCCESS = "发布成功"
    POST_FAILED = "发布失败"
    POST_NOT_FOUND = "笔记不存在"
    CONTENT_EMPTY = "内容不能为空"
    CONTENT_TOO_LONG = "内容过长"
    INVALID_CONTENT = "内容格式不正确"
    
    # 用户相关
    USER_NOT_FOUND = "用户不存在"
    USER_BLOCKED = "用户已被屏蔽"
    PROFILE_UPDATE_SUCCESS = "个人资料更新成功"
    PROFILE_UPDATE_FAILED = "个人资料更新失败"
    
    # 互动相关
    LIKE_SUCCESS = "点赞成功"
    LIKE_FAILED = "点赞失败"
    UNLIKE_SUCCESS = "取消点赞成功"
    UNLIKE_FAILED = "取消点赞失败"
    COMMENT_SUCCESS = "评论成功"
    COMMENT_FAILED = "评论失败"
    COMMENT_DELETED = "评论已删除"
    
    # 关注相关
    FOLLOW_SUCCESS = "关注成功"
    FOLLOW_FAILED = "关注失败"
    UNFOLLOW_SUCCESS = "取消关注成功"
    UNFOLLOW_FAILED = "取消关注失败"
    ALREADY_FOLLOWED = "已经关注过该用户"
    
    # 收藏相关
    COLLECT_SUCCESS = "收藏成功"
    COLLECT_FAILED = "收藏失败"
    UNCOLLECT_SUCCESS = "取消收藏成功"
    UNCOLLECT_FAILED = "取消收藏失败"
    
    # 搜索相关
    SEARCH_NO_RESULTS = "未找到相关内容"
    SEARCH_FAILED = "搜索失败"
    
    # 权限相关
    PERMISSION_DENIED = "权限不足"
    OPERATION_NOT_ALLOWED = "不允许的操作"
    
    # 网络相关
    NETWORK_ERROR = "网络连接错误"
    TIMEOUT = "请求超时"
    SERVER_ERROR = "服务器错误"
    
    # 验证相关
    VERIFICATION_REQUIRED = "需要验证"
    VERIFICATION_FAILED = "验证失败"
    VERIFICATION_CODE_SENT = "验证码已发送"
    VERIFICATION_CODE_EXPIRED = "验证码已过期"
    
    # 限制相关
    RATE_LIMIT_EXCEEDED = "请求过于频繁，请稍后再试"
    DAILY_LIMIT_REACHED = "今日操作次数已达上限"
    
    # 其他
    UNKNOWN_ERROR = "未知错误"
    OPERATION_CANCELLED = "操作已取消"
    PLEASE_TRY_AGAIN = "请重试"