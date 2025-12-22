class CustomerInfo:
    """Customer informations."""
    
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
        
    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Email: {self.email}")
        
    def update_email(self, new_email):
        self.email = new_email
        print("Email updated successfully.")