class MemrefConstInfo:
    def __init__(self, var, mem, off, op, const_num):
        self.var = var
        self.mem = mem
        self.off = off
        self.op = op
        self.const_num = const_num

    def __str__(self):
        return f"{self.var}.{self.mem} at {self.off} {self.op} {self.const_num}"