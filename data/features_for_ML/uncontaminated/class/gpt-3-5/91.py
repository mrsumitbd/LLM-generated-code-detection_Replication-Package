class Args:
    def __init__(self, *args):
        self.args = args

    def get_args(self):
        return self.args

    def add_arg(self, arg):
        self.args += (arg,)

    def remove_arg(self, arg):
        self.args = tuple(filter(lambda x: x != arg, self.args))

    def clear_args(self):
        self.args = ()