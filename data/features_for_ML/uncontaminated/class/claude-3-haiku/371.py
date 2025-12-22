class SeedEXState:
    """席德强化E释放的**当前**状态"""

    def __init__(self, seed_ex_duration: float, seed_ex_damage: float, seed_ex_range: float):
        self.seed_ex_duration = seed_ex_duration
        self.seed_ex_damage = seed_ex_damage
        self.seed_ex_range = seed_ex_range

    def get_seed_ex_duration(self) -> float:
        return self.seed_ex_duration

    def get_seed_ex_damage(self) -> float:
        return self.seed_ex_damage

    def get_seed_ex_range(self) -> float:
        return self.seed_ex_range

    def set_seed_ex_duration(self, new_duration: float) -> None:
        self.seed_ex_duration = new_duration

    def set_seed_ex_damage(self, new_damage: float) -> None:
        self.seed_ex_damage = new_damage

    def set_seed_ex_range(self, new_range: float) -> None:
        self.seed_ex_range = new_range