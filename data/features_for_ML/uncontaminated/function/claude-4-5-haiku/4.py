import re
from fractions import Fraction

def fix_fracs(string):
    def replace_frac(match):
        frac_str = match.group(0)
        # Parse the fraction string (e.g., "3/4" -> Fraction(3, 4))
        parts = frac_str.split('/')
        numerator = int(parts[0])
        denominator = int(parts[1])
        frac = Fraction(numerator, denominator)
        # Return the fraction in the format "Fraction(numerator, denominator)"
        return f"Fraction({frac.numerator}, {frac.denominator})"
    
    # Find all fractions in the string (pattern: digits/digits)
    result = re.sub(r'\d+/\d+', replace_frac, string)
    return result