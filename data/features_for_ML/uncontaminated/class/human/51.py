
class _User:
        def __init__(self, data):
            self.id = data.get("id", None)
            self.username = data.get("username", None)
            self.avatar = data.get("avatar", None)

        def __repr__(self):
            return str(self.__dict__)