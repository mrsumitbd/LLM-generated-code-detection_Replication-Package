import ray

class RuntimeEnv:
    """A typed wrapper around the ray runtime environment class.

    We use this for clarity when setting up the runtime environment for a pipeline.
    """

    def __init__(self, **kwargs):
        self.env_dict = kwargs

    def to_ray_runtime_env(self) -> ray.runtime_env.RuntimeEnv:
        return ray.runtime_env.RuntimeEnv(**self.env_dict)

    def format(self) -> str:
        return str(self.env_dict)