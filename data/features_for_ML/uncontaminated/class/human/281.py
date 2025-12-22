from dataclasses import MISSING
from . import mdp

class CommandsCfg:
    """Command terms for the MDP."""

    ee_pose: mdp.UniformPoseCommandCfg = MISSING