def connect():
        instance = GamepadDriver.instance()
        instance._connect()
        return instance