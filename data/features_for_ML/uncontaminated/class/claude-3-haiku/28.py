class JaneCoreSkillStrikeCritRateBonusRecord:
    def __init__(self, skill_name, base_crit_rate, bonus_crit_rate, bonus_duration):
        self.skill_name = skill_name
        self.base_crit_rate = base_crit_rate
        self.bonus_crit_rate = bonus_crit_rate
        self.bonus_duration = bonus_duration

    def get_total_crit_rate(self):
        return self.base_crit_rate + self.bonus_crit_rate

    def get_bonus_duration_remaining(self, time_elapsed):
        return max(0, self.bonus_duration - time_elapsed)

    def __str__(self):
        return f"Skill: {self.skill_name}, Base Crit Rate: {self.base_crit_rate:.2f}, Bonus Crit Rate: {self.bonus_crit_rate:.2f}, Bonus Duration: {self.bonus_duration:.2f}"