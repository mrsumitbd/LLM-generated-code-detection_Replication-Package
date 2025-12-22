def list_molalities_minerals(sr3):
    """
    Returns the lists of spatially distributed molalities and minerals.
    """
    molalities = []
    minerals = []
    for i in range(len(sr3)):
        for j in range(len(sr3[i])):
            for k in range(len(sr3[i][j])):
                molalities.append(sr3[i][j][k][0])
                minerals.append(sr3[i][j][k][1])
    return molalities, minerals