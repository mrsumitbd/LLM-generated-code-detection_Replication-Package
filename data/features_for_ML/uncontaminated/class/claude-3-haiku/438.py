class CustomerInfo:
    """Customer informations."""

    def __init__(self, name, email, phone, address):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    def update_email(self, new_email):
        self.email = new_email

    def update_phone(self, new_phone):
        self.phone = new_phone

    def update_address(self, new_address):
        self.address = new_address

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Phone: {self.phone}")
        print(f"Address: {self.address}")