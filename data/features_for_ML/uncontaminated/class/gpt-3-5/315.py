class ControlSignal:
    
    def __init__(self) -> None:
        self.in_loop = False

    def start(self) -> None:
        self.in_loop = True

    def stop(self) -> None:
        self.in_loop = False

    def is_in_loop(self) -> bool:
        return self.in_loop