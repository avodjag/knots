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
    
    def toText(self, var):
        poly = ''
        for exp in sorted(self.powers):
            if self.powers[exp] != 0:
                if exp < 0:
                    poly = poly + ' - '
                elif exp > 0 and poly != '':
                    poly = poly + ' + '
                poly = poly + var + '^' + str(exp)
        if poly == '':
            poly = '0'
        return poly

# constants
A = laurent({1 : 1})
B = laurent({-1 : 1})
Ao = laurent({2 : -1, -2 : -1})
        
    
