from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any


@dataclass
class PoseObservationsCfg:
    """Observation specifications for the environment."""

    # Basic pose components
    include_position: bool = True
    include_orientation: bool = True

    # Velocity components
    include_velocity: bool = False
    include_angular_velocity: bool = False

    # Acceleration components
    include_acceleration: bool = False
    include_angular_acceleration: bool = False

    # Joint state components
    include_joint_positions: bool = False
    include_joint_velocities: bool = False
    include_joint_torques: bool = False

    # Additional custom observation names
    custom_observations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the configuration."""
        return asdict(self)

    @classmethod
    def from_dict(cls, cfg: Dict[str, Any]) -> "PoseObservationsCfg":
        """Create a configuration instance from a dictionary."""
        return cls(**cfg)

    def get_observation_keys(self) -> List[str]:
        """Return a list of observation names based on the configuration."""
        keys: List[str] = []

        if self.include_position:
            keys.extend(["position_x", "position_y", "position_z"])
        if self.include_orientation:
            keys.extend(["orientation_w", "orientation_x", "orientation_y", "orientation_z"])
        if self.include_velocity:
            keys.extend(["velocity_x", "velocity_y", "velocity_z"])
        if self.include_angular_velocity:
            keys.extend(["angular_velocity_x", "angular_velocity_y", "angular_velocity_z"])
        if self.include_acceleration:
            keys.extend(["acceleration_x", "acceleration_y", "acceleration_z"])
        if self.include_angular_acceleration:
            keys.extend(["angular_acceleration_x", "angular_acceleration_y", "angular_acceleration_z"])
        if self.include_joint_positions:
            keys.append("joint_positions")
        if self.include_joint_velocities:
            keys.append("joint_velocities")
        if self.include_joint_torques:
            keys.append("joint_torques")

        keys.extend(self.custom_observations)
        return keys

    def get_observation_dim(self) -> int:
        """Return the dimensionality of the observation vector."""
        dim = 0
        if self.include_position:
            dim += 3
        if self.include_orientation:
            dim += 4
        if self.include_velocity:
            dim += 3
        if self.include_angular_velocity:
            dim += 3
        if self.include_acceleration:
            dim += 3
        if self.include_angular_acceleration:
            dim += 3
        if self.include_joint_positions:
            dim += 1
        if self.include_joint_velocities:
            dim += 1
        if self.include_joint_torques:
            dim += 1
        # Custom observations are assumed to be scalar each
        dim += len(self.custom_observations)
        return dim

    def __repr__(self) -> str:
        """Human‑readable representation."""
        cfg = self.to_dict()
        items = ", ".join(f"{k}={v!r}" for k, v in cfg.items())
        return f"{self.__class__.__name__}({items})"