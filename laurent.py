class laurent:

    def __init__(self, powers):
        self.powers = powers

    def __add__(self, other):
        summed = {exp : self.powers.get(exp, 0) + other.powers.get(exp, 0) for exp in set(self.powers) | set(other.powers)}
        return laurent(summed)

    def __mul__(self, other):
        mult = {}
        for j in list(self.powers):
            for k in list(other.powers):
                mult[j+k] = mult.get(j+k, 0) + self.powers[j]*other.powers[k]
        return laurent(mult)
    
def toText(poly, var = 't'):
    text = ''
    for exp in sorted(poly.powers):
        if poly.powers[exp] != 0:
            if poly.powers[exp] < 0:
                text = text + ' - '
            elif poly.powers[exp] > 0 and text != '':
                text = text + ' + '
            if exp == 0:
                text = text + '1'
            elif abs(poly.powers[exp]) > 1:
                text = text + str(abs(poly.powers[exp])) + '*' + var + '^' + str(exp)
            else:
                text = text + var + '^' + str(exp)
    if text == '':
        text = '0'
    if text[0] == ' ':
        text = text[1:]
    return text

def substitution(poly):
    substPowers = {exp/4 : poly.powers[exp] for exp in poly.powers.keys()}
    return laurent(substPowers)

def power(poly, exp):
    res = one
    for i in range(exp):
        res = res*poly
    return res

# constants
A = laurent({1 : 1})
B = laurent({-1 : 1})
C = laurent({2 : -1, -2 : -1})
one = laurent({0 : 1})
        
    
