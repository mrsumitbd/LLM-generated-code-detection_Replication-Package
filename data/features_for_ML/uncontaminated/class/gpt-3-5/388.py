from typing import List

class InstancePool:
    def __init__(self):
        self.instances = []

    def add_instance(self, instance):
        self.instances.append(instance)

    def get_instances(self):
        return self.instances

class InstancePoolManager:
    """Manager for `InstancePool`"""

    def __init__(self, pool: InstancePool):
        self.pool = pool

    def __enter__(self):
        return self.pool

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass