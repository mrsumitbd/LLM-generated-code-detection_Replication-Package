class RuntimeEnv:
    """A typed wrapper around the ray runtime environment class.

    We use this for clarity when setting up the runtime environment for a pipeline.
    """

    def __init__(self, **kwargs):
        self._env_dict = kwargs

    def to_ray_runtime_env(self) -> ray.runtime_env.RuntimeEnv:
        return ray.runtime_env.RuntimeEnv(**self._env_dict)

    def format(self) -> str:
        if not self._env_dict:
            return "RuntimeEnv()"
        
        items = []
        for key, value in self._env_dict.items():
            if isinstance(value, str):
                items.append(f"{key}='{value}'")
            else:
                items.append(f"{key}={value}")
        
        return f"RuntimeEnv({', '.join(items)})"