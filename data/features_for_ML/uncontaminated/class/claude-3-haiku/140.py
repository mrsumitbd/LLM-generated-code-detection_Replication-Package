class _User:
    def __init__(self, data):
        self.name = data['name']
        self.email = data['email']
        self.age = data['age']
        self.is_admin = data['is_admin']

    def __repr__(self):
        return f"_User(name='{self.name}', email='{self.email}', age={self.age}, is_admin={self.is_admin})"