class UserSearchRefinement:
    def __init__(self):
        self.min_age = None
        self.max_age = None
        self.gender = None
        self.location = None

    def set_min_age(self, min_age):
        self.min_age = min_age

    def set_max_age(self, max_age):
        self.max_age = max_age

    def set_gender(self, gender):
        self.gender = gender

    def set_location(self, location):
        self.location = location

    def get_min_age(self):
        return self.min_age

    def get_max_age(self):
        return self.max_age

    def get_gender(self):
        return self.gender

    def get_location(self):
        return self.location