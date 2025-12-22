class WatchDog:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Buddy')
        self.breed = kwargs.get('breed', 'Labrador')
        self.age = kwargs.get('age', 5)
        self.weight = kwargs.get('weight', 50)
        self.is_active = kwargs.get('is_active', True)

    def bark(self):
        print(f"{self.name} the {self.breed} is barking!")

    def sit(self):
        if self.is_active:
            print(f"{self.name} the {self.breed} is sitting.")
        else:
            print(f"{self.name} the {self.breed} is too tired to sit.")

    def fetch(self, item):
        if self.is_active:
            print(f"{self.name} the {self.breed} fetched the {item}.")
        else:
            print(f"{self.name} the {self.breed} is too lazy to fetch the {item}.")

    def get_age(self):
        return self.age

    def get_weight(self):
        return self.weight