class Select:
    
    def __init__(self, *args):
        self.items = list(args)
    
    def add(self, item):
        self.items.append(item)
    
    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
    
    def display(self):
        for item in self.items:
            print(item)