def filterset(illuminant,
              values=[0, 0, 0],
              edges=[510,495,605,590],
              transitions=[10,10,10,10],
              ):
    
    def filter_value(wavelength, edge, transition, value):
        if wavelength < edge - transition:
            return 0
        elif wavelength < edge:
            return value * ((wavelength - (edge - transition)) / transition)
        elif wavelength < edge + transition:
            return value * (1 - ((wavelength - edge) / transition))
        else:
            return 0
    
    result = [0, 0, 0]
    for i in range(3):
        for j in range(4):
            result[i] += filter_value(illuminant, edges[j], transitions[j], values[i])
    
    return result