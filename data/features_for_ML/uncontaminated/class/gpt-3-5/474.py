class PhysicsState:
    """Everything you need for the engine to take an action and step physics."""
    
    def __init__(self, position, velocity, acceleration):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        
    def update(self, time_step):
        self.velocity += self.acceleration * time_step
        self.position += self.velocity * time_step
        
    def set_position(self, position):
        self.position = position
        
    def set_velocity(self, velocity):
        self.velocity = velocity
        
    def set_acceleration(self, acceleration):
        self.acceleration = acceleration