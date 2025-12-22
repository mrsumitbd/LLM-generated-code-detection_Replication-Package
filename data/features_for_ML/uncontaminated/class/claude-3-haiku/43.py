class CommandGetDbSchemas:
    def __init__(self):
        self.schemas = []

    def Unpack(self, any_message):
        try:
            self.schemas = any_message.split(',')
        except (AttributeError, TypeError):
            self.schemas = []