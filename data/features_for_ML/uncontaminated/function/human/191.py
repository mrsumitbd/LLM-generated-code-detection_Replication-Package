def list_molalities_minerals(sr3):
    """
    Returns the lists of spatially distributed molalities and minerals.
    """

    # Get the GEM indices between the brackets in MOLALITY(1) etc
    ind_mol = [int(name[name.find('(') + 1:name.find(')')]) for name in sr3.sp_name if 'MOLALITY' in name]
    molalities = [sr3.comp_name[i - 1] for i in ind_mol]

    # Get the GEM indices between the brackets in MINERAL(1) etc
    ind_min = [int(name[name.find('(') + 1:name.find(')')]) for name in sr3.sp_name if 'MINERAL' in name]
    minerals = [sr3.comp_name[i - 1] for i in ind_min]

    return molalities, minerals