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

    def step(self, action):
        # Implement step function logic here
        pass

    def reset(self):
        # Implement reset function logic here
        pass

    def getobs(self):
        # Implement getobs function logic here
        pass