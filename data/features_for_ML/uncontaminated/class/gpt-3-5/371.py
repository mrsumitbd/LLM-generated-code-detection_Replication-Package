class SeedEXState:
    """席德强化E释放的**当前**状态"""

    def __init__(self, health, energy, is_stunned):
        self.health = health
        self.energy = energy
        self.is_stunned = is_stunned

    def take_damage(self, damage):
        self.health -= damage

    def restore_health(self, amount):
        self.health += amount

    def use_energy(self, amount):
        self.energy -= amount

    def restore_energy(self, amount):
        self.energy += amount

    def stun(self):
        self.is_stunned = True

    def remove_stun(self):
        self.is_stunned = False