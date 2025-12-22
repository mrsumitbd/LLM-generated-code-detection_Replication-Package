class HelpSteer3Dataset:
    """HelpSteer3 preference dataset for DPO training."""

    def __init__(self) -> None:
        self.data = []

    def add_preference(self, user_id, item_id, preference):
        self.data.append((user_id, item_id, preference))

    def get_preferences(self, user_id):
        return [(u_id, i_id, pref) for u_id, i_id, pref in self.data if u_id == user_id]

# Example usage:
dataset = HelpSteer3Dataset()
dataset.add_preference(1, 'A', 5)
dataset.add_preference(1, 'B', 3)
dataset.add_preference(2, 'A', 4)
dataset.add_preference(2, 'C', 2)

print(dataset.get_preferences(1))  # Output: [(1, 'A', 5), (1, 'B', 3)]
print(dataset.get_preferences(2))  # Output: [(2, 'A', 4), (2, 'C', 2)]