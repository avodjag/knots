import copy

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
A = {1 : 1}
B = {-1 : 1}
Ao = {2 : -1, -2 : -1}
N = 0



def krat(p, q):
    s = {}
    for j in list(p):
        for k in list(q):
            s[j+k] = s.get(j+k, 0) + p[j]*q[k]
    return s
    

def plus(p, q):
    return {exp : p.get(exp, 0) + q.get(exp, 0) for exp in set(p) | set(q)}

def writhe(uzel):
    w = 0
    n = len(uzel)
    for kriz in uzel:
        a, b, c, d = kriz
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

def spoj(uzel, co, kam):
    knot = copy.deepcopy(uzel)
    for i in range(len(knot)):
        for j in range(4):
            if knot[i][j] == co:
                knot[i][j] = kam
    return knot

def dic2pol(d):
    for e in sorted(d):
        if d[e] != 0:
            print(d[e], "(A^", e, ")", end = ' ')
    return

def tisk(d):
    for e in sorted(d):
        if d[e] != 0:
            print(d[e], "(t^", e/4, ")", end = ' ')
    return

def invariantuj(poly, uzel):
    w = writhe(uzel)
    C = {-3*w: 1}
    return krat(C, poly)



def bracket(uzel, flag):
    global N
    if flag == 0:
        N=N+1
    knot = copy.deepcopy(uzel)
    if flag:
        if flag == 1 and knot == []:
            poly = {}
            poly[0] = 1
            return poly
        poly = krat(Ao, bracket(knot, flag-1))
        #print(uzel, " s kruznici ma polynom ")
        #dic2pol(poly)
        #print()
        #print("vracim " ,uzel, " s kruznici")
        #dic2pol(poly)
        #print(" ")
        return poly
    poly = {}
    if knot == []:
        poly[0] = 1
        #print("jenom kruznice")
        return poly
    a, b, c, d = knot.pop();
    flag1, flag2 = 0, 0
    if (a == b or c == d) or (a == d and b == c):   # ohyby sem a tam
        flag1 = 1
    if (a == d or b == c) or (a == b and c == d):   # ohyby sem a tam
        flag2 = 1
    if a == b and c == d:
        flag1 = 2
    if a == d and b == c:
        flag2 = 2
    if d == a:
        knot1 = spoj(knot, b, a)
        knot1 = spoj(knot1, c, d)
    else:
        knot1 = spoj(knot, a, b)
        knot1 = spoj(knot1, d, c)
    if a == b:
        knot2 = spoj(knot, d, a)
        knot2 = spoj(knot2, c, b)
    else:
        knot2 = spoj(knot, a, d)
        knot2 = spoj(knot2, b, c)
    poly = plus(krat(A, bracket(knot1, flag1)), krat(B, bracket(knot2, flag2)))
    #print(uzel, " ma polynom ")
    #dic2pol(poly)
    #print(" ")
    #inv = invariantuj(poly, uzel)
    #inv = invariantuj(poly, uzel)
    #print(uzel)
    #dic2pol(poly)
    #print("writhe ", writhe(uzel))
    #tisk(inv)
    #print(" ")
    return poly

def jones(uzel):
    br = bracket(uzel, 0)
    inv = invariantuj(br, uzel)
    tisk(inv)
    return inv

def posloup(pred):
    t_2 = {2:1}
    c = {-1/2: -1, 3/2:1}
    return plus(krat(pred, t_2), c)
    


#a =bracket(trefoil, False)  
#dic2pol(a)
