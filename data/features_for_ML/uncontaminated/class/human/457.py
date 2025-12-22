
class XHSMessages:
    """小红书相关消息常量"""
    
    # 成功消息
    PUBLISH_SUCCESS = "笔记发布成功"
    UPLOAD_SUCCESS = "文件上传成功"
    LOGIN_SUCCESS = "登录成功"
    
    # 错误消息
    PUBLISH_FAILED = "笔记发布失败"
    UPLOAD_FAILED = "文件上传失败"
    LOGIN_REQUIRED = "需要登录"
    NETWORK_ERROR = "网络连接错误"
    FILE_NOT_FOUND = "文件不存在"
    INVALID_FILE_FORMAT = "不支持的文件格式"
    
    # 警告消息
    LONG_CONTENT_WARNING = "内容较长，可能影响发布效果"
    TOO_MANY_IMAGES_WARNING = "图片数量过多"
    LARGE_FILE_WARNING = "文件过大，上传可能较慢"