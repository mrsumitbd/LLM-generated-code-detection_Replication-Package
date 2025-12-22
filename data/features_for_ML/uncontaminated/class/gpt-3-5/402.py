class Digit:
    """
    DIGIT类
    """

    def __init__(self, digit=None, chntext=None):
        self.digit = digit
        self.chntext = chntext

    def digit2chntext(self):
        digit_chntext_map = {
            '0': '零',
            '1': '一',
            '2': '二',
            '3': '三',
            '4': '四',
            '5': '五',
            '6': '六',
            '7': '七',
            '8': '八',
            '9': '九'
        }
        if self.digit is not None:
            self.chntext = digit_chntext_map.get(str(self.digit), 'Invalid Digit')
        return self.chntext