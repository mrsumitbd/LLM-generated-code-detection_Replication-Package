class TimeweaverApBonusRecord:
    
    def __init__(self):
        self.ap_bonus_records = {}

    def add_ap_bonus_record(self, player_id, ap_bonus):
        if player_id in self.ap_bonus_records:
            self.ap_bonus_records[player_id] += ap_bonus
        else:
            self.ap_bonus_records[player_id] = ap_bonus

    def get_ap_bonus_record(self, player_id):
        return self.ap_bonus_records.get(player_id, 0)

    def remove_ap_bonus_record(self, player_id):
        if player_id in self.ap_bonus_records:
            del self.ap_bonus_records[player_id]

    def clear_all_ap_bonus_records(self):
        self.ap_bonus_records = {}