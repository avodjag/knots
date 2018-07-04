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
K = 1
counter = {n+1: 0 for n in range(100)}

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
    if abs(b-d) == 1:
        if b > d:
            return 1
        else:
            return -1
    else:
        if b > d:
            return -1
        else:
            return 1

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
            if crossing[:4] not in PDknot:
                PDknot.append(crossing[:4])
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

def twoSide(knot):
    for e in knot.keys():
        a, b, c, d, s= knot[e][0]
        if a != e and a in knot[e][1]:
            return e
        if b != e and b in knot[e][1]:
            return e
        if c != e and c in knot[e][1]:
            return e
        if d != e and d in knot[e][1]:
            return e
    return -1

def threeSide(knot):
    edge = -1
    cross = []
    for e in knot.keys():
        c1 = knot[e][0]  # udelat to pak prohozene
        c2 = knot[e][1]

        i1 = c1.index(e)
        i2 = c2.index(e)

        e1 = c1[(i1+1)%4]
        e2 = c2[(i2-1)%4]

        if knot[e1][0] == c1:
            c10 = knot[e1][1]
        else:
            c10 = knot[e1][0]

        if knot[e2][0] == c2:
            c20 = knot[e2][1]
        else:
            c20 = knot[e2][0]

        if c10 != c20:
            continue

        if e1%2 == e2%2:
            return e1
        else:
            edge = e1
            cross = c10
            
    for e in knot.keys():
        c1 = knot[e][1]  # udelat to pak prohozene
        c2 = knot[e][0]

        i1 = c1.index(e)
        i2 = c2.index(e)

        e1 = c1[(i1+1)%4]
        e2 = c2[(i2-1)%4]

        if knot[e1][0] == c1:
            c10 = knot[e1][1]
        else:
            c10 = knot[e1][0]

        if knot[e2][0] == c2:
            c20 = knot[e2][1]
        else:
            c20 = knot[e2][0]

        if c10 != c20:
            continue

        if e1%2 == e2%2:
            return e1
        else:
            edge = e1
            cross = c10
    if edge == -1:
        print(dic_to_PD(knot))
        for e in knot.keys():
            print(e)
            print(knot[e])
    else:
        print("nekdy")
    if knot[edge][0] == cross:
        tmp = knot[edge][1]
        knot[edge][1] = cross
        knot[edge][0] = tmp
    return edge
            

def bracket(prev_knot, reid2, looped):

    #reid2 = False
    
    knot = copy.deepcopy(prev_knot)
    #print(dic_to_PD(knot))
    poly = laurent({})
    
    global N
    global M
    global K
    #global counter

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
    if N == 1:
        print(len(dic_to_PD(knot)))
    
    #if K < N:
     #   K = 2*K
      #  print(N)
       # print(len(dic_to_PD(knot)))
    if N%10000 == 0:
        print(N)
        print(len(dic_to_PD(knot)))

    #counter[len(knot)] = counter[len(knot)] + 1
    #print(len(knot))
    
    #edge = next(iter(knot))
    edge = twoSide(knot)

    if edge == -1:
        edge = threeSide(knot)
    if edge == -1:
        print(dic_to_PD(knot))

    #if not (twoSide(knot) or threeSide(knot)):
        #print("smth wrong")
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
k50 = [[1, 40, 2, 41], [23, 3, 24, 2], [3, 43, 4, 42], [4, 26, 5, 25], [66, 5, 67, 6], [61, 7, 62, 6], [86, 7, 87, 8], [8, 81, 9, 82], [9, 48, 10, 49], [49, 10, 50, 11], [11, 90, 12, 91], [91, 12, 92, 13], [13, 92, 14, 93], [14, 51, 15, 52], [15, 59, 16, 58], [29, 17, 30, 16], [17, 97, 18, 96], [18, 36, 19, 35], [72, 20, 73, 19], [73, 20, 74, 21], [21, 100, 22, 1], [22, 39, 23, 40], [24, 42, 25, 41], [26, 43, 27, 44], [68, 27, 69, 28], [77, 29, 78, 28], [30, 57, 31, 58], [94, 31, 95, 32], [53, 32, 54, 33], [33, 54, 34, 55], [55, 34, 56, 35], [36, 97, 37, 98], [70, 38, 71, 37], [38, 76, 39, 75], [44, 68, 45, 67], [78, 46, 79, 45], [46, 59, 47, 60], [88, 47, 89, 48], [89, 51, 90, 50], [52, 94, 53, 93], [56, 95, 57, 96], [79, 60, 80, 61], [85, 62, 86, 63], [63, 82, 64, 83], [64, 84, 65, 83], [84, 66, 85, 65], [69, 76, 70, 77], [71, 99, 72, 98], [74, 99, 75, 100], [80, 88, 81, 87]]

k49 = [[1, 38, 2, 39], [35, 2, 36, 3], [40, 3, 41, 4], [33, 5, 34, 4], [5, 59, 6, 58], [57, 7, 58, 6], [7, 57, 8, 56], [59, 9, 60, 8], [42, 10, 43, 9], [10, 32, 11, 31], [96, 11, 97, 12], [12, 86, 13, 85], [13, 86, 14, 87], [69, 15, 70, 14], [88, 15, 89, 16], [16, 68, 17, 67], [90, 18, 91, 17], [91, 18, 92, 19], [66, 20, 67, 19], [93, 21, 94, 20], [21, 65, 22, 64], [22, 51, 23, 52], [23, 51, 24, 50], [25, 25, 26, 24], [26, 49, 27, 50], [80, 28, 81, 27], [28, 54, 29, 53], [74, 29, 75, 30], [61, 31, 62, 30], [32, 42, 33, 41], [39, 35, 40, 34], [36, 98, 37, 97], [98, 38, 1, 37], [60, 43, 61, 44], [44, 55, 45, 56], [76, 46, 77, 45], [77, 46, 78, 47], [78, 48, 79, 47], [79, 48, 80, 49], [52, 81, 53, 82], [54, 76, 55, 75], [73, 63, 74, 62], [63, 83, 64, 82], [65, 93, 66, 92], [68, 89, 69, 90], [70, 88, 71, 87], [71, 94, 72, 95], [83, 73, 84, 72], [84, 96, 85, 95]]
# 168040 vs 35910
# rozbite na k49, k50
#mozna na vsech uzlech, kde je jenom trojice?
#jones([[1, 10, 2, 11], [18, 6, 1, 5], [4, 20, 5, 19], [38, 12, 19, 11], [27, 15, 28, 14], [28, 35, 29, 36], [15, 34, 16, 35], [39, 33, 40, 32], [25, 42, 26, 39], [31, 25, 32, 24], [22, 22, 23, 7], [9, 7, 10, 6], [2, 37, 3, 38], [13, 37, 14, 36], [33, 26, 34, 27], [23, 41, 24, 40], [3, 13, 4, 12], [20, 17, 21, 18], [16, 30, 17, 29], [21, 8, 8, 9], [41, 30, 42, 31]]) ma 19?
# so kdyz je tri stena ta venkovni?
# k50 = 3088913
