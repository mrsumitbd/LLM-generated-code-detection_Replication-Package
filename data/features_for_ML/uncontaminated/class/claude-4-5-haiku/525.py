class AlfworldWorker:
    """
    Ray remote actor that replaces the worker function.
    Each actor holds one environment instance.
    """

    def __init__(self, config, seed, base_env=None, env_type=None, single_gamefile=None, is_train=True, eval_dataset='eval_in_distribution'):
        self.config = config
        self.seed = seed
        self.base_env = base_env
        self.env_type = env_type
        self.single_gamefile = single_gamefile
        self.is_train = is_train
        self.eval_dataset = eval_dataset
        
        self.env = None
        self.last_observation = None
        self.episode_step = 0
        self.episode_reward = 0.0
        
        self._initialize_env()

    def _initialize_env(self):
        """Initialize the environment based on configuration."""
        if self.base_env is not None:
            self.env = self.base_env
        else:
            import gym
            if self.env_type:
                self.env = gym.make(self.env_type)
            else:
                self.env = gym.make(self.config.get('env_id', 'alfworld-v0'))
        
        if hasattr(self.env, 'seed'):
            self.env.seed(self.seed)
        
        self.last_observation = self.env.reset()
        self.episode_step = 0
        self.episode_reward = 0.0

    def step(self, action):
        """
        Execute one step in the environment.
        
        Args:
            action: The action to take in the environment
            
        Returns:
            tuple: (observation, reward, done, info)
        """
        observation, reward, done, info = self.env.step(action)
        
        self.last_observation = observation
        self.episode_step += 1
        self.episode_reward += reward
        
        if done:
            info['episode_reward'] = self.episode_reward
            info['episode_step'] = self.episode_step
        
        return observation, reward, done, info

    def reset(self):
        """
        Reset the environment.
        
        Returns:
            observation: The initial observation after reset
        """
        self.last_observation = self.env.reset()
        self.episode_step = 0
        self.episode_reward = 0.0
        
        return self.last_observation

    def getobs(self):
        """
        Get the current observation without taking a step.
        
        Returns:
            observation: The current observation
        """
        return self.last_observation