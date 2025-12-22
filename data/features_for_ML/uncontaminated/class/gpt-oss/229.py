import json
import ray
from typing import Any, Dict


class RuntimeEnv:
    """A typed wrapper around the ray runtime environment class.

    We use this for clarity when setting up the runtime environment for a pipeline.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Create a RuntimeEnv from keyword arguments that match the Ray runtime
        environment specification.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments that will be stored as the runtime
            environment configuration. Typical keys include ``packages``,
            ``env_vars``, ``resources``, ``working_dir``, ``python``, etc.
        """
        self._config: Dict[str, Any] = dict(kwargs)

    def to_ray_runtime_env(self) -> ray.runtime_env.RuntimeEnv:
        """
        Convert this wrapper into a Ray RuntimeEnv object.

        Returns
        -------
        ray.runtime_env.RuntimeEnv
            A Ray RuntimeEnv instance constructed from the stored configuration.
        """
        return ray.runtime_env.RuntimeEnv(self._config)

    def format(self) -> str:
        """
        Return a human‑readable JSON representation of the runtime environment.

        Returns
        -------
        str
            A pretty‑printed JSON string of the configuration dictionary.
        """
        return json.dumps(self._config, indent=2, sort_keys=True)