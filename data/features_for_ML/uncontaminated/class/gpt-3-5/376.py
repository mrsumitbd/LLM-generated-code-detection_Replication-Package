import random

class RandomTrial:
    """A dummy trial class for generating random parameters."""

    def suggest_categorical(self, name, choices):
        return random.choice(choices)

    def suggest_int(self, name, low, high, step=1, log=False):
        if log:
            low = max(1, low)
            low = round(math.log(low, step))
            high = round(math.log(high, step))
            return int(step ** random.randint(low, high))
        else:
            return random.randint(low, high)

    def suggest_float(self, name, low, high, step=None, log=False):
        if log:
            low = max(1, low)
            low = math.log(low, step)
            high = math.log(high, step)
            return step ** random.uniform(low, high)
        else:
            return random.uniform(low, high)