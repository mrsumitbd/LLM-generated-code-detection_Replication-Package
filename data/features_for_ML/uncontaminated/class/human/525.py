from openmanus_rl.environments.env_package.alfworld.alfworld.agents.environment import get_environment

class AlfworldWorker:
    """
    Ray remote actor that replaces the worker function.
    Each actor holds one environment instance.
    """
    
    def __init__(self, config, seed, base_env=None, env_type=None, single_gamefile=None, is_train=True, eval_dataset='eval_in_distribution'):
        if base_env is not None:
            # Legacy path: share a base_env and instantiate sub-env from it
            self.env = base_env.init_env(batch_size=1)
        else:
            # Unique path: each worker binds to exactly one gamefile
            assert env_type is not None, "env_type is required when base_env is None"
            BaseEnvCls = get_environment(env_type)
            game_files_override = [single_gamefile] if single_gamefile is not None else None
            be = BaseEnvCls(config, train_eval='train' if is_train else eval_dataset, game_files=game_files_override)
            self.env = be.init_env(batch_size=1)
        self.env.seed(seed)
    
    def step(self, action):
        """Execute a step in the environment"""
        actions = [action] 
        
        obs, scores, dones, infos = self.env.step(actions)
        infos['observation_text'] = obs
        return obs, scores, dones, infos
    
    def reset(self):
        """Reset the environment"""
        obs, infos = self.env.reset()
        infos['observation_text'] = obs
        return obs, infos
    
    def getobs(self):
        """Get current observation image"""
        image = get_obs_image(self.env)
        image = image.cpu()  
        return image