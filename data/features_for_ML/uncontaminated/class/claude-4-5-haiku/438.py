class CustomerInfo:
    """Customer informations."""
    
    def __init__(self, customer_id: str, name: str, email: str, phone: str = "", address: str = ""):
        """Initialize customer information.
        
        Args:
            customer_id: Unique identifier for the customer
            name: Customer's full name
            email: Customer's email address
            phone: Customer's phone number (optional)
            address: Customer's address (optional)
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
    
    def __str__(self) -> str:
        """Return string representation of customer info."""
        return f"CustomerInfo(id={self.customer_id}, name={self.name}, email={self.email}, phone={self.phone}, address={self.address})"
    
    def __repr__(self) -> str:
        """Return detailed string representation."""
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        """Check equality based on customer_id."""
        if not isinstance(other, CustomerInfo):
            return False
        return self.customer_id == other.customer_id
    
    def update_email(self, email: str) -> None:
        """Update customer's email address.
        
        Args:
            email: New email address
        """
        self.email = email
    
    def update_phone(self, phone: str) -> None:
        """Update customer's phone number.
        
        Args:
            phone: New phone number
        """
        self.phone = phone
    
    def update_address(self, address: str) -> None:
        """Update customer's address.
        
        Args:
            address: New address
        """
        self.address = address
    
    def get_info(self) -> dict:
        """Return customer information as dictionary.
        
        Returns:
            Dictionary containing all customer information
        """
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address
        }