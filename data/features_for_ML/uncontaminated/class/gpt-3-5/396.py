class WatchDog:
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Unknown')
        self.age = kwargs.get('age', 0)
        self.breed = kwargs.get('breed', 'Unknown')
        self.color = kwargs.get('color', 'Unknown')
        self.is_trained = kwargs.get('is_trained', False)
        
    def bark(self):
        print("Woof! Woof!")
        
    def sit(self):
        print(f"{self.name} is sitting.")
        
    def roll_over(self):
        print(f"{self.name} rolled over.")
        
    def fetch(self, item):
        print(f"{self.name} fetched the {item}.")