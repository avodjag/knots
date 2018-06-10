import copy
from laurent import *

# uzly
trefoil = [[1,5,2,4],[3,1,4,6],[5,3,6,2]]
# bracket: 't^-7 - t^-3 - t^5', jones: 't^-4.0 - t^-3.0 - t^-1.0'
k6_3 = [[4,2,5,1],[8,4,9,3],[12,9,1,10],[10,5,11,6],[6,11,7,12],[2,8,3,7]]
osm = [[4,2,5,1],[8,6,1,5],[6,3,7,4],[2,7,3,8]]
pet1 = [[2,8,3,7],[4,10,5,9],[6,2,7,1],[8,4,9,3],[10,6,1,5]]


# motanice
ctyr = [[8,1,1,2],[2,7,3,8],[6,3,7,4],[4,5,5,6]]
ctyr2 = [[8,1,1,2],[2,7,3,8],[4,5,5,6],[6,3,7,4]]
troj = [[6,1,1,2],[2,5,3,6],[4,3,5,4]]
troj2 =[[6,1,1,2],[4,3,5,4],[2,5,3,6]] 
dvoj = [[4,1,1,2],[2,3,3,4]]
#loop = [[2,1,2,1]] spatna loop
loop = [[2, 1, 1, 2]]
loopp = [[1,1,2,2]]

hopf = [[1,4,2,3], [3,2,4,1]]
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
            if knot[edge] != [] and knot[edge][-1] == [a, b, c, d, s]:      # smycka, uz to tam bylo pridano
                continue
            knot[edge].append([a, b, c, d, s])
    return knot

def dic_to_PD(knot):
    PDknot = []
    for edge in knot.keys():
        for crossing in knot[edge]:
            if crossing[:5] not in PDknot:
                PDknot.append(crossing[:5])
    return PDknot

t = PD_to_dic(trefoil)
o = PD_to_dic(osm)
c = PD_to_dic(ctyr)
l = PD_to_dic(loop)

def rename(knot, what, where):    
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
        del knot[what]
        return 1
    else:
        rename(knot, what, where)
        crossing = knot[edge][0]
        if knot[what][0] == crossing:
            what_crossing = knot[what][1]
        else:
            what_crossing = knot[what][0]
        # knot[what] = []
        del knot[what]
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
        if edge not in knot:   # uz to zmizelo behem
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
    return [exp, unknots]    # ma tu byt plus ci minus?

def connect(knot, crossing, what, where):
    if knot[what][0] == crossing:
        other_crossing = knot[what][1]
    else:
        other_crossing = knot[what][0]
    
    if knot[where][0] == crossing:
        knot[where][0] = other_crossing
    else:
        knot[where][1] = other_crossing
    for neighbour in set(crossing[:4]).union(other_crossing[:4]):
        if neighbour == what:
            continue
        for j in range(len(knot[neighbour])):
            for i in range(4):
                if knot[neighbour][j][i] == what:
                    knot[neighbour][j][i] = where
    if knot[where][0] == knot[where][1]:
        knot[where] = [knot[where][0]]

def relabel_crossing(crossing, what, where):
    new_crossing = list(crossing)
    for i in range(4):
        if new_crossing[i] == what:
            new_crossing[i] = where
    return new_crossing
        

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
    D = laurent({-3*w: 1})
    return D * poly


def bracket(prev_knot, unknots, looped):
    
    knot = copy.deepcopy(prev_knot)
    #print(dic_to_PD(knot))
    poly = laurent({})
    
    global N
    if unknots > 0:
        if unknots == 1 and knot == []:
            poly = one
            return one
        poly = C * bracket(knot, unknots-1)
        print("Uzel " + str(dic_to_PD(knot)) + " ma polynom : " + toText(poly))
        return poly
    if knot == {}:
        poly = one
        print("Prazdny " + str(dic_to_PD(knot)) + " ma polynom : " + toText(poly))
        return poly
    if looped:
        exp, loop_unknots = unloop(knot)  #neni tu problem, ze nekopiruju?
        if exp != 0 or loop_unknots > 0:
            Aw = laurent({-3*exp : 1})
            #print("odmotano") #je to spatne, moc prejmenovani
            #print(dic_to_PD(knot))
            poly = Aw * power(C, unknots) * bracket(knot, 0, False)
            print("Rozmotany uzel " + str(dic_to_PD(prev_knot)) + " ma polynom : " + toText(poly))
            return poly

    N = N + 1

    edge = next(iter(knot))
    crossing = knot[edge][1]
    a, b, c, d, s = crossing
    
    unknots1, unknots2 = 0, 0

    knot1 = copy.deepcopy(knot)
    knot2 = copy.deepcopy(knot)
    
    if edge == b or edge == c:    
        connect(knot1, crossing, b, a)
        connect(knot1, relabel_crossing(crossing, b, a), c, d)
        del knot1[b]
        del knot1[c]
    else:
        connect(knot1, crossing, a, b)
        connect(knot1, relabel_crossing(crossing, a, b), d, c)
        del knot1[a]
        del knot1[d]
        
    if edge == d or edge == c:        
        connect(knot2, crossing, d, a)
        connect(knot2, relabel_crossing(crossing, d, a), c, b)
        del knot2[d]
        del knot2[c]
    else:        
        connect(knot2, crossing, a, d)
        connect(knot2, relabel_crossing(crossing,a, d), b, c)
        del knot2[a]
        del knot2[b] 

    poly = (A * bracket(knot1, unknots1, True)) + (B * bracket(knot2, unknots2, True))
    print("Uzel " + str(dic_to_PD(knot)) + " ma polynom : " + toText(poly))
    return poly

def jones(PDknot):
    knot = PD_to_dic(PDknot)
    bracket_poly = bracket(knot, 0, True)
    inv_poly = add_writhe(bracket_poly, PDknot)
    jones_poly = substitution(inv_poly)
    return toText(jones_poly)

#trefoil 
# Uzel [[3, 5, 2, 6, 1], [5, 3, 6, 2, 1]] ma polynom : t^-4 + t^-2 hopf link
# ale ma to byt '- t^-4 - t^4'
# bere asi spatne znamínko v linku


