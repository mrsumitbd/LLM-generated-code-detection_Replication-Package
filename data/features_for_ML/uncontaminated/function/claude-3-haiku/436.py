def trigger_action():
    import time
    import random

    # Simulate some action
    time.sleep(random.uniform(0.5, 2.0))

    # Return a result
    return random.randint(1, 100)