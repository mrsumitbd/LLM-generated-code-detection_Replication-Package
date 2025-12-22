class SpinnerManager:
    
    def __init__(self, console: Console, message: str = "Processing..."):
        self.console = console
        self.message = message
        self.spinner = Spinner()
    
    def start(self):
        self.console.write(self.message)
        self.spinner.start()
    
    def stop(self):
        self.spinner.stop()