class Config:
    '''
    ====== Configuration Parameters ======
    Tune these values based on your gameplay and detection needs.
    --------------------------------------
    '''

    # Detection settings
    DETECTION_THRESHOLD: float = 0.8          # Confidence threshold for detections
    MAX_DETECTION_ATTEMPTS: int = 5           # Max retries for a detection cycle
    DETECTION_TIMEOUT: float = 10.0           # Timeout (seconds) for each detection attempt

    # Gameplay settings
    MOVE_SPEED: float = 1.0                   # Units per second
    ATTACK_COOLDOWN: float = 2.0              # Seconds between attacks
    MAX_HEALTH: int = 100                     # Starting health

    # Debugging & logging
    DEBUG_MODE: bool = False
    LOG_LEVEL: str = 'INFO'                   # Options: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'

    # Environment
    ENVIRONMENT: str = 'production'           # Options: 'development', 'staging', 'production'

    @classmethod
    def load_from_env(cls):
        """
        Override configuration values with environment variables.
        Environment variable names must match the attribute names.
        """
        import os
        for attr in dir(cls):
            if attr.isupper():
                env_val = os.getenv(attr)
                if env_val is not None:
                    current_val = getattr(cls, attr)
                    try:
                        if isinstance(current_val, bool):
                            env_val = env_val.lower() in ('1', 'true', 'yes', 'on')
                        elif isinstance(current_val, int):
                            env_val = int(env_val)
                        elif isinstance(current_val, float):
                            env_val = float(env_val)
                        # else keep as string
                    except Exception:
                        pass  # keep raw string if conversion fails
                    setattr(cls, attr, env_val)

    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'<Config {attrs}>'