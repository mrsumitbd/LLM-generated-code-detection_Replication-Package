import random

class RandomTrial:
    """A dummy trial class for generating random parameters."""

    def suggest_categorical(self, name, choices):
        return random.choice(choices)

    def suggest_int(self, name, low, high, step=1, log=False):
        if log:
            import math
            log_low = math.log(low)
            log_high = math.log(high)
            value = math.exp(random.uniform(log_low, log_high))
            return int(round(value / step) * step)
        else:
            return random.randint(low, high // step) * step

    def suggest_float(self, name, low, high, step=None, log=False):
        if log:
            import math
            log_low = math.log(low)
            log_high = math.log(high)
            value = math.exp(random.uniform(log_low, log_high))
        else:
            value = random.uniform(low, high)
        
        if step is not None:
            value = round(value / step) * step
        
        return value