def create_a_coin_cell_deck():
    """
    Creates a deck of cards for the Coin Cell card game.
    Returns a list of tuples representing cards in the deck.
    Each tuple contains (value, suit) where:
    - value is a number from 1-13 (Ace, 2-10, Jack, Queen, King)
    - suit is one of: 'Hearts', 'Diamonds', 'Clubs', 'Spades'
    """
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = list(range(1, 14))
    
    deck = []
    for suit in suits:
        for value in values:
            deck.append((value, suit))
    
    return deck