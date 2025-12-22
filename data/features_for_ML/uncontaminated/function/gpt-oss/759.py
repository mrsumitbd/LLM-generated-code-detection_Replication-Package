def create_a_coin_cell_deck():
    ranks = [
        "Ace", "2", "3", "4", "5", "6", "7",
        "8", "9", "10", "Jack", "Queen", "King"
    ]
    suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
    return [f"{rank} of {suit}" for suit in suits for rank in ranks]