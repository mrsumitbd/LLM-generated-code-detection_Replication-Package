class CommandGetDbSchemas:

    def __init__(self):
        pass

    def Unpack(self, any_message):
        # Assuming any_message is a dictionary with 'schemas' key
        if 'schemas' in any_message:
            return any_message['schemas']
        else:
            return None