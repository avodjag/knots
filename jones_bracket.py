import copy
from laurent import *

# uzly
trefoil = [[1,5,2,4],[3,1,4,6],[5,3,6,2]]
k6_3 = [[4,2,5,1],[8,4,9,3],[12,9,1,10],[10,5,11,6],[6,11,7,12],[2,8,3,7]]
osm = [[4,2,5,1],[8,6,1,5],[6,3,7,4],[2,7,3,8]]
pet1 = [[2,8,3,7],[4,10,5,9],[6,2,7,1],[8,4,9,3],[10,6,1,5]]


# motanice
ctyr = [[8,1,1,2],[2,7,3,8],[6,3,7,4],[4,5,5,6]]
ctyr2 = [[8,1,1,2],[2,7,3,8],[4,5,5,6],[6,3,7,4]]
troj = [[6,1,1,2],[2,5,3,6],[4,3,5,4]]
troj2 =[[6,1,1,2],[4,3,5,4],[2,5,3,6]] 
dvoj = [[4,1,1,2],[2,3,3,4]]
loop = [[1,1,2,2]]

N = 0

def sign(PDcrossing, n):
    a, b, c, d = PDcrossing
    if a == b or c == d:
        return 1
    if a == d or b == c:
        return -1
    if b == 1 and d == 2*n:
        return 1
    if b == 2*n and d == 1:
        return -1
    if b > d:
        return 1
    else:
        return -1

def PD_to_dic(PDknot):
    n = len(PDknot)
    knot = {i+1 : [] for i in range(2*n)}
    for crossing in PDknot:
        a, b, c, d = crossing
        s = sign(crossing, n)
        for edge in crossing:
            if knot[edge] != [] and knot[edge][-1] == [a, b, c, d, s]:
                continue
            knot[edge].append([a, b, c, d, s])
    return knot

def rename(knot, what, where):    # prepojuje jenom v ostatnich, v tom mazanem nic nedela
    for i in range(len(knot[what])):
        edge = knot[what][i]
        new_edge = list(edge)
        for j in range(4):
            if new_edge[j] == what:
                new_edge[j] = where
        for j in range(4):
            neighb = edge[j]
            for k in range(len(knot[neighb])):
                if knot[neighb][k] == edge:
                    knot[neighb][k] = new_edge

def uncross(knot, loops, edge, what, where):
    if what == where:
        knot[what] = []
        return 1
    else:
        rename(knot, what, where)
        crossing = knot[edge][0]
        if knot[what][0] == crossing:
            what_crossing = knot[what][1]
        else:
            what_crossing = knot[what][0]
        knot[what] = []
        if knot[where][0] == crossing:
            if knot[where][1] == what_crossing:
                loops.append(where)
                knot[where] = [what_crossing]
            else:
                knot[where][0] = what_crossing
        return 0


def unloop(knot):
    exp = 0
    unknots = 0
    loops = []
    for edge in knot.keys():
        if len(knot[edge]) == 1:
            loops.append(edge)
    while loops != []:
        edge = loops.pop()
        if edge not in knot:
            continue
        a, b, c, d, sign = knot[edge][0]
        exp = exp + sign
        if a == b and a == edge:
            unknots = unknots + uncross(knot, loops, edge, c, d)
        if a == c and a == edge:
            unknots = unknots + uncross(knot, loops, edge, b, d)
        if a == d and a == edge:
            unknots = unknots + uncross(knot, loops, edge, b, c)
        if b == c and b == edge:
            unknots = unknots + uncross(knot, loops, edge, a, d)
        if b == d and b == edge:
            unknots = unknots + uncross(knot, loops, edge, a, c)
        if c == d and c == edge:
            unknots = unknots + uncross(knot, loops, edge, a, b)
        del knot[edge]
    return [exp, unknots]
                
        

def writhe(PDknot):
    w = 0
    n = len(PDknot)
    for crossing in PDknot:
        a, b, c, d = crossing
        w = w + sign(crossing, n)
    return w

def PDconnect(knot, what, where):
    knot = copy.deepcopy(knot)
    for i in range(len(knot)):
        for j in range(4):
            if knot[i][j] == what:
                knot[i][j] = where
    return knot

def add_writhe(poly, knot):
    w = writhe(knot)
    C = laurent({-3*w: 1})
    return C * poly


def bracket(prev_knot, unknots, looped):
    knot = dict(prev_knot)
    poly = laurent({})
    
    global N
    if unknots > 0:
        if unknots == 1 and knot == []:
            poly = one
            return one
        poly = C * bracket(knot, unknots-1)
        return poly
    if knot == []:
        poly = one
        return poly
    if looped:
        exp, loop_unknots = unloop(knot)
        if exp != 0 or loop_unknots > 0:
            Aw = laurent({-3*exp : 1})
            poly = Aw * power(Ao, unknots) * bracket(knot, 0, False)
            return poly

    N = N + 1

    edge = next(iter(knot))
    crossing = knot[edge][1]
    knot[edge] = [knot[edge[0]]]
    
    a, b, c, d, s = crossing

    # potud upraveno na dic strukturu
    
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
        knot1 = PDconnect(knot, b, a)
        knot1 = connect(knot1, c, d)
    else:
        knot1 = PDconnect(knot, a, b)
        knot1 = connect(knot1, d, c)
    if a == b:    #F
        knot2 = PDconnect(knot, d, a)
        knot2 = PDconnect(knot2, c, b)
    else:
        knot2 = PDconnect(knot, a, d)
        knot2 = PDconnect(knot2, b, c)
        
    poly = (A * bracket(knot1, unknots1, True)) + (B * bracket(knot2, unknots2, True))
    return poly

def jones(PDknot):
    knot = PD_to_dic(PDknot)
    bracket_poly = bracket(knot, 0, True)
    inv_poly = add_writhe(bracket_poly, PDknot)
    jones_poly = substitution(inv_poly)
    return toText(jones_poly)

