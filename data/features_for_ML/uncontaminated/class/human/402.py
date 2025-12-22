
class Digit:
    """
    DIGIT类
    """

    def __init__(self, digit=None, chntext=None):
        self.digit = digit
        self.chntext = chntext

    # def chntext2digit(self):
    #     return chn2num(self.chntext)

    def digit2chntext(self):
        return num2chn(self.digit, alt_two=False, use_units=False)