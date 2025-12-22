def create_a_coin_cell_deck():
    import random
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [(value, suit) for value in values for suit in suits]
    random.shuffle(deck)
    return deck