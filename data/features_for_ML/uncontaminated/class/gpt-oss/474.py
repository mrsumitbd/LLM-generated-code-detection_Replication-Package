import numpy as np

class PhysicsState:
    """Everything you need for the engine to take an action and step physics."""

    def __init__(
        self,
        position=None,
        velocity=None,
        orientation=None,
        angular_velocity=None,
        mass=1.0,
        inertia=None,
        gravity=None,
        linear_damping=0.0,
        angular_damping=0.0,
    ):
        self.position = np.array(position if position is not None else [0.0, 0.0, 0.0], dtype=float)
        self.velocity = np.array(velocity if velocity is not None else [0.0, 0.0, 0.0], dtype=float)
        self.orientation = np.array(orientation if orientation is not None else [0.0, 0.0, 0.0], dtype=float)  # Euler angles (rad)
        self.angular_velocity = np.array(angular_velocity if angular_velocity is not None else [0.0, 0.0, 0.0], dtype=float)

        self.mass = float(mass)
        self.inertia = (
            np.array(inertia, dtype=float) if inertia is not None else np.eye(3) * mass
        )
        self.gravity = np.array(gravity if gravity is not None else [0.0, -9.81, 0.0], dtype=float)

        self.linear_damping = float(linear_damping)
        self.angular_damping = float(angular_damping)

        # Accumulated forces and torques for the current time step
        self._force_accum = np.zeros(3, dtype=float)
        self._torque_accum = np.zeros(3, dtype=float)

    # ------------------------------------------------------------------
    # Force / torque application
    # ------------------------------------------------------------------
    def apply_force(self, force, point=None):
        """Apply a force to the body. If point is given, also apply torque."""
        f = np.asarray(force, dtype=float)
        self._force_accum += f
        if point is not None:
            r = np.asarray(point, dtype=float) - self.position
            self._torque_accum += np.cross(r, f)

    def apply_torque(self, torque):
        """Apply a torque to the body."""
        self._torque_accum += np.asarray(torque, dtype=float)

    # ------------------------------------------------------------------
    # Integration
    # ------------------------------------------------------------------
    def _integrate(self, dt):
        """Internal integration step."""
        # Linear dynamics
        total_force = self._force_accum + self.mass * self.gravity
        acceleration = total_force / self.mass
        self.velocity += acceleration * dt
        self.velocity *= (1.0 - self.linear_damping * dt)
        self.position += self.velocity * dt

        # Angular dynamics
        angular_acc = np.linalg.inv(self.inertia).dot(self._torque_accum)
        self.angular_velocity += angular_acc * dt
        self.angular_velocity *= (1.0 - self.angular_damping * dt)
        self.orientation += self.angular_velocity * dt

        # Reset accumulators
        self._force_accum[:] = 0.0
        self._torque_accum[:] = 0.0

    def step(self, action, dt):
        """
        Apply an action (dict with optional 'force' and 'torque') and advance the state by dt.
        """
        if action:
            if "force" in action:
                self.apply_force(action["force"])
            if "torque" in action:
                self.apply_torque(action["torque"])
        self._integrate(dt)

    # ------------------------------------------------------------------
    # State accessors
    # ------------------------------------------------------------------
    def get_state(self):
        """Return a dictionary representation of the state."""
        return {
            "position": self.position.copy(),
            "velocity": self.velocity.copy(),
            "orientation": self.orientation.copy(),
            "angular_velocity": self.angular_velocity.copy(),
        }

    def set_state(self, state):
        """Set the state from a dictionary."""
        if "position" in state:
            self.position[:] = state["position"]
        if "velocity" in state:
            self.velocity[:] = state["velocity"]
        if "orientation" in state:
            self.orientation[:] = state["orientation"]
        if "angular_velocity" in state:
            self.angular_velocity[:] = state["angular_velocity"]

    def copy(self):
        """Return a deep copy of the physics state."""
        new_state = PhysicsState(
            position=self.position.copy(),
            velocity=self.velocity.copy(),
            orientation=self.orientation.copy(),
            angular_velocity=self.angular_velocity.copy(),
            mass=self.mass,
            inertia=self.inertia.copy(),
            gravity=self.gravity.copy(),
            linear_damping=self.linear_damping,
            angular_damping=self.angular_damping,
        )
        new_state._force_accum = self._force_accum.copy()
        new_state._torque_accum = self._torque_accum.copy()
        return new_state

    # ------------------------------------------------------------------
    # Energy utilities
    # ------------------------------------------------------------------
    def kinetic_energy(self):
        """Return the total kinetic energy."""
        lin_ke = 0.5 * self.mass * np.dot(self.velocity, self.velocity)
        ang_ke = 0.5 * np.dot(self.angular_velocity, self.inertia.dot(self.angular_velocity))
        return lin_ke + ang_ke

    def potential_energy(self):
        """Return the gravitational potential energy."""
        return self.mass * np.dot(self.gravity, self.position)

    def total_energy(self):
        """Return the sum of kinetic and potential energy."""
        return self.kinetic_energy() + self.potential_energy()

    # ------------------------------------------------------------------
    # Miscellaneous
    # ------------------------------------------------------------------
    def __repr__(self):
        return (
            f"PhysicsState(position={self.position}, velocity={self.velocity}, "
            f"orientation={self.orientation}, angular_velocity={self.angular_velocity})"
        )