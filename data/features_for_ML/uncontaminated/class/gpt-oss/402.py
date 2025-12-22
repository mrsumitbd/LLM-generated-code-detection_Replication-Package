class Digit:
    """
    DIGIT类
    """

    _digit_to_chn = {
        '0': '零',
        '1': '一',
        '2': '二',
        '3': '三',
        '4': '四',
        '5': '五',
        '6': '六',
        '7': '七',
        '8': '八',
        '9': '九',
    }

    def __init__(self, digit=None, chntext=None):
        """
        初始化 Digit 对象。

        :param digit: 需要转换的整数或字符串形式的数字
        :param chntext: 已经是中文数字的字符串（可选）
        """
        self.digit = digit
        self.chntext = chntext

    def digit2chntext(self):
        """
        将 self.digit 转换为中文数字字符串，并存入 self.chntext。

        :return: 中文数字字符串
        """
        if self.digit is None:
            raise ValueError("digit is not set")

        # 处理整数或字符串
        if isinstance(self.digit, int):
            num_str = str(self.digit)
        elif isinstance(self.digit, str):
            num_str = self.digit
        else:
            raise TypeError("digit must be int or str")

        # 处理负数
        negative = False
        if num_str.startswith('-'):
            negative = True
            num_str = num_str[1:]

        # 转换每一位
        chn_parts = []
        for ch in num_str:
            if ch not in self._digit_to_chn:
                raise ValueError(f"invalid digit character: {ch}")
            chn_parts.append(self._digit_to_chn[ch])

        result = ''.join(chn_parts)
        if negative:
            result = '负' + result

        self.chntext = result
        return result