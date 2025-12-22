class PoseObservationsCfg:
    """Observation specifications for the environment."""
    
    def __init__(self, num_poses=1, pose_dim=3):
        self.num_poses = num_poses
        self.pose_dim = pose_dim
        
    def set_num_poses(self, num_poses):
        self.num_poses = num_poses
        
    def set_pose_dim(self, pose_dim):
        self.pose_dim = pose_dim
        
    def get_num_poses(self):
        return self.num_poses
    
    def get_pose_dim(self):
        return self.pose_dim