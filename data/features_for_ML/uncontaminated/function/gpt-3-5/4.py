def fix_fracs(string):
    import fractions
    import re

    def replace_fraction(match):
        return str(fractions.Fraction(match.group(0)))

    return re.sub(r'\d+/\d+', replace_fraction, string)