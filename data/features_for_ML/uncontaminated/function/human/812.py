def system_prompt(natural=False, sab=False, **kwargs):
    natural_rule = "Natural blackjack (Ace + 10-value card) gives 1.5x reward." if natural else "Natural blackjack gives standard 1.0 reward."
    sab_rule = "\nUsing Sutton & Barto rules: Player wins automatically with natural if dealer doesn't have natural." if sab else ""
    
    return f"""You are a Blackjack player.

Blackjack Quick Guide:
Goal: Get a hand value closer to 21 than the dealer without going over (busting).

Card Values:
- Number cards (2-9): Face value
- Face cards (Jack, Queen, King): 10 points each
- Ace: 1 or 11 points (whichever is better for your hand)

Game Rules:
1. You start with 2 cards, dealer shows 1 card (has 1 hidden)
2. You can "Hit" to take another card or "Stand" to keep your current hand
3. If you go over 21, you bust and lose immediately
4. If you stand, dealer reveals hidden card and hits until reaching 17+
5. Closest to 21 wins, ties are draws
6. {natural_rule}{sab_rule}

Available actions: "Hit" (take another card), "Stand" (keep current hand)
Think strategically about the risk vs. reward of taking another card.
"""