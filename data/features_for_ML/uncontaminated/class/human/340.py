
class Encoder:
        def __init__(self):
            self.conv1 = self.Conv(stride=(1,))
            self.conv2 = self.Conv(stride=(2,))

        class Conv:
            def __init__(self, stride):
                self.stride = stride