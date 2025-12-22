class Args:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    
    def __repr__(self):
        args_str = ', '.join(repr(arg) for arg in self.args)
        kwargs_str = ', '.join(f'{k}={repr(v)}' for k, v in self.kwargs.items())
        all_args = ', '.join(filter(None, [args_str, kwargs_str]))
        return f'Args({all_args})'
    
    def __str__(self):
        return self.__repr__()
    
    def __getitem__(self, index):
        if isinstance(index, int):
            return self.args[index]
        return self.kwargs[index]
    
    def __setitem__(self, index, value):
        if isinstance(index, int):
            args_list = list(self.args)
            args_list[index] = value
            self.args = tuple(args_list)
        else:
            self.kwargs[index] = value
    
    def __len__(self):
        return len(self.args) + len(self.kwargs)
    
    def __iter__(self):
        return iter(self.args)
    
    def __contains__(self, item):
        return item in self.args or item in self.kwargs.values()
    
    def __eq__(self, other):
        if not isinstance(other, Args):
            return False
        return self.args == other.args and self.kwargs == other.kwargs
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __add__(self, other):
        if isinstance(other, Args):
            return Args(*(self.args + other.args), **{**self.kwargs, **other.kwargs})
        return NotImplemented
    
    def __mul__(self, n):
        if isinstance(n, int):
            return Args(*(self.args * n), **self.kwargs)
        return NotImplemented
    
    def __rmul__(self, n):
        return self.__mul__(n)
    
    def get(self, key, default=None):
        return self.kwargs.get(key, default)
    
    def keys(self):
        return self.kwargs.keys()
    
    def values(self):
        return list(self.args) + list(self.kwargs.values())
    
    def items(self):
        return self.kwargs.items()