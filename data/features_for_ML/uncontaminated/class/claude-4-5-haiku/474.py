class PhysicsState:
    """Everything you need for the engine to take an action and step physics."""
    
    def __init__(self, position=None, velocity=None, acceleration=None, 
                 rotation=None, angular_velocity=None, mass=1.0, 
                 forces=None, torques=None, friction=0.0, restitution=0.5):
        """
        Initialize a physics state.
        
        Args:
            position: Vector3 or tuple of (x, y, z) coordinates
            velocity: Vector3 or tuple of velocity components
            acceleration: Vector3 or tuple of acceleration components
            rotation: Quaternion or tuple representing rotation
            angular_velocity: Vector3 or tuple of angular velocity
            mass: Scalar mass value
            forces: List of force vectors acting on the object
            torques: List of torque vectors acting on the object
            friction: Coefficient of friction
            restitution: Coefficient of restitution (bounciness)
        """
        self.position = position if position is not None else (0.0, 0.0, 0.0)
        self.velocity = velocity if velocity is not None else (0.0, 0.0, 0.0)
        self.acceleration = acceleration if acceleration is not None else (0.0, 0.0, 0.0)
        self.rotation = rotation if rotation is not None else (0.0, 0.0, 0.0, 1.0)
        self.angular_velocity = angular_velocity if angular_velocity is not None else (0.0, 0.0, 0.0)
        self.mass = mass
        self.forces = forces if forces is not None else []
        self.torques = torques if torques is not None else []
        self.friction = friction
        self.restitution = restitution
    
    def apply_force(self, force):
        """Apply a force to the object."""
        self.forces.append(force)
    
    def apply_torque(self, torque):
        """Apply a torque to the object."""
        self.torques.append(torque)
    
    def clear_forces(self):
        """Clear all accumulated forces."""
        self.forces = []
    
    def clear_torques(self):
        """Clear all accumulated torques."""
        self.torques = []
    
    def get_total_force(self):
        """Calculate total force from all applied forces."""
        if not self.forces:
            return (0.0, 0.0, 0.0)
        total = [sum(f[i] for f in self.forces) for i in range(3)]
        return tuple(total)
    
    def get_total_torque(self):
        """Calculate total torque from all applied torques."""
        if not self.torques:
            return (0.0, 0.0, 0.0)
        total = [sum(t[i] for t in self.torques) for i in range(3)]
        return tuple(total)
    
    def update_acceleration(self):
        """Update acceleration based on total force and mass."""
        total_force = self.get_total_force()
        if self.mass > 0:
            self.acceleration = tuple(f / self.mass for f in total_force)
        else:
            self.acceleration = (0.0, 0.0, 0.0)
    
    def step(self, dt):
        """
        Step the physics simulation forward by dt seconds.
        
        Args:
            dt: Time step in seconds
        """
        self.update_acceleration()
        
        # Update velocity based on acceleration
        self.velocity = tuple(
            self.velocity[i] + self.acceleration[i] * dt 
            for i in range(3)
        )
        
        # Update position based on velocity
        self.position = tuple(
            self.position[i] + self.velocity[i] * dt 
            for i in range(3)
        )
        
        # Clear forces and torques for next step
        self.clear_forces()
        self.clear_torques()
    
    def __repr__(self):
        return (f"PhysicsState(position={self.position}, velocity={self.velocity}, "
                f"acceleration={self.acceleration}, rotation={self.rotation}, "
                f"mass={self.mass})")