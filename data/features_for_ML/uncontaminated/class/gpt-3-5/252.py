class BaseBuffRecord:
    """基础记录Class"""

    def __init__(self):
        self.buff_dict = {}

    def add_buff(self, buff_name, buff_value):
        self.buff_dict[buff_name] = buff_value

    def remove_buff(self, buff_name):
        if buff_name in self.buff_dict:
            del self.buff_dict[buff_name]

    def get_buff_value(self, buff_name):
        return self.buff_dict.get(buff_name, None)

    def clear_buffs(self):
        self.buff_dict = {}