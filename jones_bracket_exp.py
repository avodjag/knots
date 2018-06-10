import copy
from laurent import *

# uzly
trefoil = [[1,5,2,4],[3,1,4,6],[5,3,6,2]]
k6_3 = [[4,2,5,1],[8,4,9,3],[12,9,1,10],[10,5,11,6],[6,11,7,12],[2,8,3,7]]
osm = [[4,2,5,1],[8,6,1,5],[6,3,7,4],[2,7,3,8]]

# motanice
pet1 = [[2,8,3,7],[4,10,5,9],[6,2,7,1],[8,4,9,3],[10,6,1,5]]
ctyr = [[8,1,1,2],[2,7,3,8],[6,3,7,4],[4,5,5,6]]
ctyr2 = [[8,1,1,2],[2,7,3,8],[4,5,5,6],[6,3,7,4]]
troj = [[6,1,1,2],[2,5,3,6],[4,3,5,4]]
troj2 =[[6,1,1,2],[4,3,5,4],[2,5,3,6]] 
dvoj = [[4,1,1,2],[2,3,3,4]]
#loop = [[2,1,2,1]]   # nefunguje pro loop, asi bo ta loop neexistuje
loop = [[2,1,1,2]]


N = 0

def writhe(knot):
    w = 0
    n = len(knot)
    for cross in knot:
        a, b, c, d = cross
        if a == b or c == d:
            w = w + 1
            continue
        if a == d or b == c:
            w = w - 1
            continue
        if b == 1 and d == 2*n:
            w = w + 1
            continue
        if b == 2*n and d == 1:
            w = w - 1
            continue
        if b > d:
            w = w + 1
        else:
            w = w - 1
    return w

def connect(knot, what, where):
    knot = copy.deepcopy(knot)
    for i in range(len(knot)):
        for j in range(4):
            if knot[i][j] == what:
                knot[i][j] = where
    return knot

def addWrithe(poly, knot):
    w = writhe(knot)
    D = laurent({-3*w: 1})
    return D * poly


def bracket(givenKnot, unknots):
    knot = copy.deepcopy(givenKnot)
    poly = laurent({})
    global N
    if unknots == 0:
        N=N+1
    if unknots > 0:
        if unknots == 1 and knot == []:
            poly = one
            return one
        poly = C * bracket(knot, unknots-1)
        return poly
    if knot == []:
        poly = one
        return poly
    
    a, b, c, d = knot.pop();
    unknots1, unknots2 = 0, 0

    if a == b and c == d:    #A
        unknots1 = 2
    elif (a == b or c == d) or (a == d and b == c):  #B
        unknots1 = 1
    if a == d and b == c:     #C
        unknots2 = 2
    elif (a == d or b == c) or (a == b and c == d):   #D
        unknots2 = 1
        
    if d == a:   #E
        knot1 = connect(knot, b, a)
        knot1 = connect(knot1, c, d)
    else:
        knot1 = connect(knot, a, b)
        knot1 = connect(knot1, d, c)
    if a == b:    #F
        knot2 = connect(knot, d, a)
        knot2 = connect(knot2, c, b)
    else:
        knot2 = connect(knot, a, d)
        knot2 = connect(knot2, b, c)
        
    poly = (A * bracket(knot1, unknots1)) + (B * bracket(knot2, unknots2))
    return poly

def jones(knot):
    bracketPoly = bracket(knot, 0)
    invPoly = addWrithe(bracketPoly, knot)
    jonesPoly = substitution(invPoly)
    return toText(jonesPoly)

