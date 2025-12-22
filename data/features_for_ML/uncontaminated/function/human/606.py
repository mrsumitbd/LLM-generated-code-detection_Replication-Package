import colour
from agx_emulsion.config import SPECTRAL_SHAPE, ENLARGER_STEPS

def filterset(illuminant,
              values=[0, 0, 0],
              edges=[510,495,605,590],
              transitions=[10,10,10,10],
              ):
    total_filter = create_combined_dichroic_filter(illuminant.wavelengths,
                                                  filtering_amount_percent=values,
                                                  transitions=transitions,
                                                  edges=edges)
    values = illuminant*total_filter
    filtered_illuminant = colour.SpectralDistribution(values, domain=SPECTRAL_SHAPE)
    return filtered_illuminant