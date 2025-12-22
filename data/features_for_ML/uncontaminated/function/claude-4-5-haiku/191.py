def list_molalities_minerals(sr3):
    """
    Returns the lists of spatially distributed molalities and minerals.
    """
    molalities = []
    minerals = []
    
    if sr3 is None:
        return molalities, minerals
    
    # Extract molalities from aqueous species
    if hasattr(sr3, 'aqueous_species'):
        for species in sr3.aqueous_species():
            if hasattr(species, 'molality'):
                molalities.append(species.molality())
    
    # Extract mineral amounts
    if hasattr(sr3, 'minerals'):
        for mineral in sr3.minerals():
            if hasattr(mineral, 'amount'):
                minerals.append(mineral.amount())
    
    return molalities, minerals