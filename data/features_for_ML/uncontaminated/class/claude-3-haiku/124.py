class Dummy:
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.class_attr = 'dummy'
        cls.class_method = classmethod(lambda cls: print(f"This is a class method of {cls.__name__}"))
        cls.static_method = staticmethod(lambda: print("This is a static method"))

    def __init__(self, value):
        self.instance_attr = value

    def instance_method(self):
        print(f"This is an instance method of {type(self).__name__}")