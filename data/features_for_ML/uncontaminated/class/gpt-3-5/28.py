class JaneCoreSkillStrikeCritRateBonusRecord:
    
    def __init__(self):
        self.strike_crit_rate_bonus = 0.0

    def set_strike_crit_rate_bonus(self, bonus):
        self.strike_crit_rate_bonus = bonus

    def get_strike_crit_rate_bonus(self):
        return self.strike_crit_rate_bonus

# Example usage:
# record = JaneCoreSkillStrikeCritRateBonusRecord()
# record.set_strike_crit_rate_bonus(0.1)
# print(record.get_strike_crit_rate_bonus())