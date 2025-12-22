import random
import math

class RandomTrial:
    """A dummy trial class for generating random parameters."""

    def suggest_categorical(self, name, choices):
        """Return a random choice from the provided list."""
        if not choices:
            raise ValueError(f"No choices provided for categorical parameter '{name}'.")
        return random.choice(choices)

    def suggest_int(self, name, low, high, step=1, log=False):
        """Return a random integer in [low, high] respecting step and log options."""
        if low > high:
            raise ValueError(f"Low ({low}) must be <= high ({high}) for parameter '{name}'.")
        if step <= 0:
            raise ValueError(f"Step must be positive for parameter '{name}'.")
        if log:
            # Sample log-uniformly: choose exponent uniformly between log(low) and log(high)
            if low <= 0:
                raise ValueError(f"Low must be > 0 for log sampling of parameter '{name}'.")
            log_low = math.log(low)
            log_high = math.log(high)
            val = math.exp(random.uniform(log_low, log_high))
            # Round to nearest integer
            val = int(round(val))
            # Clamp to bounds
            val = max(low, min(high, val))
            return val
        else:
            # Compute number of steps
            n_steps = (high - low) // step + 1
            idx = random.randint(0, n_steps - 1)
            return low + idx * step

    def suggest_float(self, name, low, high, step=None, log=False):
        """Return a random float in [low, high] respecting step and log options."""
        if low > high:
            raise ValueError(f"Low ({low}) must be <= high ({high}) for parameter '{name}'.")
        if log:
            if low <= 0:
                raise ValueError(f"Low must be > 0 for log sampling of parameter '{name}'.")
            log_low = math.log(low)
            log_high = math.log(high)
            val = math.exp(random.uniform(log_low, log_high))
            # Clamp to bounds
            val = max(low, min(high, val))
            return val
        else:
            val = random.uniform(low, high)
            if step is not None:
                # Round to nearest multiple of step
                val = round((val - low) / step) * step + low
                # Clamp to bounds
                val = max(low, min(high, val))
            return val