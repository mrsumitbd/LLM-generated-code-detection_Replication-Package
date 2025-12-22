def fix_fracs(string):
    fractions = string.split()
    result = []
    for fraction in fractions:
        if '/' in fraction:
            num, den = fraction.split('/')
            num, den = int(num), int(den)
            gcd = gcd_recursive(num, den)
            result.append(f"{num//gcd}/{den//gcd}")
        else:
            result.append(fraction)
    return ' '.join(result)

def gcd_recursive(a, b):
    if b == 0:
        return a
    return gcd_recursive(b, a % b)