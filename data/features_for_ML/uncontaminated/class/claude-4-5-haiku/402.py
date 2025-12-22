class Digit:
    """
    DIGIT类
    """

    def __init__(self, digit=None, chntext=None):
        self.digit = digit
        self.chntext = chntext
        self._digit_map = {
            '0': '零', '1': '一', '2': '二', '3': '三', '4': '四',
            '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'
        }
        self._chntext_map = {
            '零': '0', '一': '1', '二': '2', '三': '3', '四': '4',
            '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'
        }

    def digit2chntext(self):
        if self.digit is None:
            return None
        
        result = ''
        digit_str = str(self.digit)
        
        for char in digit_str:
            if char in self._digit_map:
                result += self._digit_map[char]
            else:
                result += char
        
        self.chntext = result
        return result