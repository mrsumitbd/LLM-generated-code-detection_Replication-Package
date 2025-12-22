class PhysicsState:
    """Everything you need for the engine to take an action and step physics."""

    def __init__(self, position, velocity, acceleration, mass, friction_coefficient):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass
        self.friction_coefficient = friction_coefficient

    def update(self, time_delta):
        self.velocity += self.acceleration * time_delta
        self.position += self.velocity * time_delta
        self.acceleration = self.calculate_acceleration()

    def calculate_acceleration(self):
        force = -self.friction_coefficient * self.mass * self.velocity
        return force / self.mass

    def apply_force(self, force):
        self.acceleration += force / self.mass