class DummyHook:
    def __init__(self):
        self.is_hooked = False

    def hook(self):
        if not self.is_hooked:
            self.is_hooked = True
            print("Hooked")

    def unhook(self):
        if self.is_hooked:
            self.is_hooked = False
            print("Unhooked")