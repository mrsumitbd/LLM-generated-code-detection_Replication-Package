class TimeweaverApBonusRecord:
    def __init__(self, player_name, ap_bonus, bonus_date):
        self.player_name = player_name
        self.ap_bonus = ap_bonus
        self.bonus_date = bonus_date

    def get_player_name(self):
        return self.player_name

    def get_ap_bonus(self):
        return self.ap_bonus

    def get_bonus_date(self):
        return self.bonus_date

    def __str__(self):
        return f"{self.player_name} received {self.ap_bonus} AP bonus on {self.bonus_date}"