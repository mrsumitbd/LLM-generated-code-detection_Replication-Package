import xax
from ksim.curriculum import Curriculum, CurriculumState
from jaxtyping import Array, PRNGKeyArray, PyTree
from ksim.types import (
    Action,
    Histogram,
    LoggedTrajectory,
    Metadata,
    Metrics,
    PhysicsData,
    PhysicsModel,
    PhysicsState,
    RewardState,
    Trajectory,
)

class RolloutEnvState:
    """Per-environment variables for the rollout loop."""

    commands: xax.FrozenDict[str, PyTree]
    physics_state: PhysicsState
    randomization_dict: xax.FrozenDict[str, Array]
    model_carry: PyTree
    reward_carry: xax.FrozenDict[str, Array]
    obs_carry: xax.FrozenDict[str, PyTree]
    obs_bias_rngs: xax.FrozenDict[str, PRNGKeyArray | None]
    curriculum_state: CurriculumState
    rng: PRNGKeyArray