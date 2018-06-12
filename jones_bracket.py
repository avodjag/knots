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
M = 0

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
    #if what == 9:
        #print("FKFJHHHHHHHHHHHHHSKJFDHK")
        #print("kam: " + str(where))
        #print(str(dic_to_PD(knot)) )
        #print("edge: " + str(edge))
    if what == where:
        del knot[what]
        if len(knot.keys()) == 1:
            return 0
        else:    # vznika vedlejsi kruznice a je tam nejaky zbytek
            return 1
    else:                   #odtud je problem
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
        else:
            if knot[where][0] == what_crossing:
                loops.append(where)
                knot[where] = [what_crossing]
            else:
                knot[where][1] = what_crossing
        return 0

def loopSign(crossing):
    a, b, c, d, s = crossing
    if a == b or c == d:
        return 1
    else:
        return -1


def unloop(knot):
    E = one
    unknots = 0
    loops = []
    for edge in knot.keys():
        if len(knot[edge]) == 1:
            loops.append(edge)  
    while loops != []:
        #print(str(dic_to_PD(knot)) )
        #print("loops")
        #print(loops)
        edge = loops.pop()
        #print("jsem na hrane " + str(edge))
        #if dic_to_PD(knot) == [[9, 5, 5, 9, 1], [3, 9, 9, 3, 1]]:
            #for k in knot.keys():
                #print("hrana " + str(k))
                #print(knot[k])
        if edge not in knot:   # uz to zmizelo behem
            continue
        a, b, c, d, s = knot[edge][0]
        sign = loopSign(knot[edge][0])
        F = laurent({sign*3: -1})
        E = E*F
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
    return [E, unknots]   

def connect(knot, crossing, what, where):
    if where not in knot:
        print(str(where) + " where tam neni")
        print(str(dic_to_PD(knot)) )
    if what not in knot:
        print(str(what) + " what tam neni")
        print(str(dic_to_PD(knot)) )
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
    if w%2 == 0:
        D = laurent({-3*w: 1})
    else:
        D = laurent({-3*w: -1})
    return D * poly

def isReidTwo(knot, edge):
    #if len(knot[edge]) == 1:
     #   print(dic_to_PD(knot))
      #  print(edge)
       # print(knot[edge])
    cross1 = knot[edge][0]
    cross2 = knot[edge][1]

    if cross1[1] == cross2[1]:
        if cross1[2] == cross2[0]:
            return 1   
        if cross1[0] == cross2[2]:
            return 2
    if cross1[3] == cross2[3]:
        if cross1[2] == cross2[0]:
            return 3
        if cross1[0] == cross2[2]:
            return 4
    return 0

#musi uz byt unlooped
def reidTwo(knot):
    unknots = 0
    looped = False
    changed = False
    edges = []
    toDel = []
    for edge in list(knot.keys()):

        if looped:
            break
        
        if edge in toDel:
            continue 
        code = isReidTwo(knot, edge)
        
        if not code:
            continue

        changed = True
        
        cross1 = knot[edge][0]
        cross2 = knot[edge][1]
        
        if code == 1:
            a = cross1[3]
            b = cross1[1]
            c = cross2[3]
            x = cross1[0]
            y = cross1[2]
            z = cross2[2]                    
        if code == 2:
            a = cross1[2]
            b = cross1[0]
            c = cross2[0]
            x = cross1[3]
            y = cross1[1]
            z = cross2[3]
        if code == 3:
            a = cross1[0]
            b = cross1[2]
            c = cross2[2]
            x = cross1[1]
            y = cross1[3]
            z = cross2[1]
        if code == 4:
            a = cross1[1]
            b = cross1[3]
            c = cross2[1]
            x = cross1[2]
            y = cross1[0]
            z = cross2[0]

        if a == c:    # jenom smazat
            unknots = unknots + 1
        else:
            rename(knot, a, c)    #a - > c
            
            cross1 = knot[edge][0]
            cross2 = knot[edge][1]

            if knot[a][0] == cross1:
                aCross = knot[a][1]
            else:
                aCross = knot[a][0]

            if knot[c][0] == cross2:
                if knot[c][1] == aCross:
                    knot[c] = [aCross]
                    looped = True
                else:
                    knot[c][0] = aCross
            else:
                if knot[c][0] == aCross:
                    knot[c] = [aCross]
                    looped = True
                else:
                    knot[c][1] = aCross


        if x == z:    # jenom smazat
            unknots = unknots + 1
        else:            
            rename(knot, x, z)   
            cross1 = knot[edge][0]
            cross2 = knot[edge][1]

            if knot[x][0] == cross1:
                xCross = knot[x][1]
            else:
                xCross = knot[x][0]

            if knot[z][0] == cross2:
                if knot[z][1] == xCross:
                    knot[z] = [xCross]
                    looped = True
                else:
                    knot[z][0] = xCross
            else:
                if knot[z][0] == xCross:
                    knot[z] = [xCross]
                    looped = True
                else:
                    knot[z][1] = xCross

        toDel = toDel + [a, b, x, y]
        
        del knot[a]
        del knot[b]
        del knot[x]
        del knot[y]

    return [changed, looped, unknots]
            
            

def bracket(prev_knot, reid2, looped):
    
    knot = copy.deepcopy(prev_knot)
    #print(dic_to_PD(knot))
    poly = laurent({})
    
    global N
    global M

    M = M + 1
    
    if knot == {}:
        poly = one
        #print("Prazdny " + str(dic_to_PD(knot)) + " ma polynom : " + toText(poly))
        return poly

    if looped:
        E, loop_unknots = unloop(knot)
        if E != one or loop_unknots > 0:
            #Aw = laurent({-3*exp : 1})
            #print("odmotano") #je to spatne, moc prejmenovani
            #print(dic_to_PD(knot))
            poly = E * power(C, loop_unknots) * bracket(knot, True, False)
            #print("Rozmotany uzel " + str(dic_to_PD(prev_knot)) + " ma polynom : " + toText(poly))
            return poly
        
    if reid2:
        changed, reidLooped, reidUnknots = reidTwo(knot)
        looped = max(reidLooped, looped)
        if changed:
             if knot == {} and reidUnknots > 0:
                 poly = power(C, reidUnknots-1)
             else:
                 poly = power(C, reidUnknots) * bracket(knot, False, looped)
             return poly

    N = N + 1
    
    edge = next(iter(knot))
    crossing = knot[edge][1]
    a, b, c, d, s = crossing
    
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

    poly = (A * bracket(knot1, True, True)) + (B * bracket(knot2, True, True))
    #print("Uzel " + str(dic_to_PD(knot)) + " ma polynom : " + toText(poly))
    return poly

def jones(PDknot):
    knot = PD_to_dic(PDknot)
    bracket_poly = bracket(knot, True, True)
    inv_poly = add_writhe(bracket_poly, PDknot)
    jones_poly = substitution(inv_poly)
    return toText(jones_poly)

def pbracket(PDknot):
    knot = PD_to_dic(PDknot)
    bracket_poly = bracket(knot, True, True)
    return toText(bracket_poly, 'A')

# problem [[2,11,3,12],[4,9,5,10],[5,19,6,18],[7,15,8,14],[10,1,11,2],[12,3,13,4],[13,17,14,16],[15,9,16,8],[17,1,18,20],[19,7,20,6]]
# taky [[1,8,2,9],[3,18,4,19],[5,12,6,13],[7,10,8,11],[9,2,10,3],[11,6,12,7],[14,20,15,19],[16,14,17,13],[17,4,18,5],[20,16,1,15]]
# vlastne tam, kde se to pouzije
k = [[1,4,2,3], [2,4,1,3]]
