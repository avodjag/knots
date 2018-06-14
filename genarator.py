import random


def randomPoints(n):
    points = []
    xs = []
    ys = []
    while len(points) != n:
        x = random.randrange(100*n)
        y = random.randrange(100*n)
        if x not in xs and y not in ys:
            points.append([x, y])
            xs.append(x)
            ys.append(y)
    return points

def determinant3(matrix):
    r1, r2, r3 = matrix
    det = r1[0] * r2[1] * r3[2] + r1[1] * r2[2] * r3[0] + r1[2] * r2[0] * r3[1]
    det = det - r1[2] * r2[1] * r3[0] + r1[1] * r2[0] * r3[2] + r1[0] * r2[2] * r3[1]
    return det

# d kladne: napravo, zaporne: nalevo
def side(line, X):
    A, B = line
    u = [X[0]-A[0], X[1]-A[1]]
    v = [B[0]-A[0], B[1]-A[1]]
    d = u[0]*v[1]-u[1]*v[0]
    return d

# po smeru rucicek
def inTriangle(triangle, X):
    A, B, C = triangle
    d = side([A,B], X)
    e = side([B,C], X)
    f = side([C,A], X)
    if d >= 0 and e >= 0 and f >= 0:
        return True
    return False

# na primce proste nechavam, bo by s tim slo pohnout, ackoli tam budou dvojite hrany
# po smeru rucicek
def convexHull(points):
    if len(points) < 3:
        return points
    p = sorted(points)
    ho = [p[0], p[1]]
    for i in range(2, len(points)):
        d = side([ho[-2], ho[-1]], p[i])
        if d >= 0:
            ho.append(p[i])
            continue
        ho = ho[:-1]
        while len(ho) > 1:
            d = side([ho[-2], ho[-1]], p[i])
            if d >= 0:
                break
            ho = ho[:-1]
        ho.append(p[i])
    lo = [p[0], p[1]]
    for i in range(2, len(points)):
        d = side([lo[-2], lo[-1]], p[i])
        if d <= 0:
            lo.append(p[i])
            continue
        lo = lo[:-1]
        while len(lo) > 1:
            d = side([lo[-2], lo[-1]], p[i])
            if d <= 0:
                break
            lo = lo[:-1]
        lo.append(p[i])

    ol = list(reversed(lo))
    hull = ho + ol[1:-1]
    return hull

def star(X, points):
    ho = []
    do = []
    for P in points:
        if P[1] > X[1]:
            ho.append(P)
        else:
            do.append(P)

    for i in range(len(ho)):
        for j in range(i, len(ho)):
            A = ho[j]
            flag = True
            for k in range(i, len(ho)):
                B = ho[k]
                d = side([X, A], B)
                if d < 0:
                    flag = False
                    break
            if flag:
                tmp = ho[i]
                ho[i] = A
                ho[j] = tmp

    for i in range(len(do)):
        for j in range(i, len(do)):
            A = do[j]
            flag = True
            for k in range(i, len(do)):
                B = do[k]
                d = side([X, A], B)
                if d < 0:
                    flag = False
                    break
            if flag:
                tmp = do[i]
                do[i] = A
                do[j] = tmp
                
    return ho + do

# po smeru, [0, i, i+1]
def triangPoly(polygon):
    n = len(polygon)
    triang = []
    for i in range(1, n-1):
        triang.append([polygon[0], polygon[i], polygon[i+1]])
    return triang


def triangulation(points):
    hull = convexHull(points)
    triang = triangPoly(hull)
    for P in points:
        if P in hull:
            continue
        for tr in triang:
            if inTriangle(tr, P):
                break
        A, B, C = tr
        triang.remove(tr)
        triang.append([A, B, P])
        triang.append([B, C, P])
        triang.append([C, A, P])
    return triang
    

def isInCircumricle(X, triangle):
    A, B, C = triangle
    r1 = [A[0]-X[0], A[1]-X[1], (A[0]-X[0])*(A[0]-X[0]) + (A[1]-X[1])*(A[1]-X[1])]
    r2 = [B[0]-X[0], B[1]-X[1], (B[0]-X[0])*(B[0]-X[0]) + (B[1]-X[1])*(B[1]-X[1])]
    r3 = [C[0]-X[0], C[1]-X[1], (C[0]-X[0])*(C[0]-X[0]) + (C[1]-X[1])*(C[1]-X[1])]
    det = determinant([r1, r2, r3])
    if det == 0:
        return False
    return True

# chcu sousedni vrcholy serazene po smeru rucicek
def triangToGraph(triang, points):
    n = len(points)
    G = [ [] for i in range(n)]
    H = [ [] for i in range(n)]
    for tr in triang:
        A, B, C = tr
        
        i = points.index(A)
        if B not in  G[i]:
            G[i].append(B)
        if C not in  G[i]:
            G[i].append(C)
            
        i = points.index(B)
        if A not in  G[i]:
            G[i].append(A)
        if C not in  G[i]:
            G[i].append(C)
            
        i = points.index(C)
        if A not in  G[i]:
            G[i].append(A)
        if B not in  G[i]:
            G[i].append(B)

    # pridat trizeni po smeru hodinovych rucicek
    # seradit horni a dolni
    # a bude to


    for i in range(n):
        P = points[i]
        G[i] = star(P, G[i])

    for i in range(n):
        for v in G[i]:
            H[i].append(points.index(v))

    return [G, H]



def makeEdges(G):
    n = len(G)
    edges = []
    for i in range(n):
        for v in G[i]:
            e = [min(i, v), max(i, v)]            
            if e not in edges:
                edges.append(e)
    return edges

def unchecked(order):
    for i in range(len(order)):
        if order[i][0] == -1 or order[i][1] == -1:
            return i
    return -1


def graphToKnot(G):
    # kazde hrane priradit ty sousedni
    # pak vybrat nahodny vrchol
    # prochazet a v kazdem vybrat nahodne orientaci

    n = len(G)    
    edges = makeEdges(G)
    m = len(edges)

    crossings = []

    for e in edges:
        u, v = e
        
        unbr = G[u]
        k = len(unbr)        

        ui = unbr.index(v)
        ai = unbr[(ui+1)%k]
        a = edges.index([min(ai, u), max(ai, u)])
        di = unbr[(ui-1)%k]
        d = edges.index([min(di, u), max(di, u)])

        vnbr = G[v]
        l = len(vnbr)

        vi = vnbr.index(u)
        ci = vnbr[(vi+1)%l]
        c = edges.index([min(ci, v), max(ci, v)])
        bi = vnbr[(vi-1)%l]
        b = edges.index([min(bi, v), max(bi, v)])

        crossings.append([a, b, c, d])
    #print(crossings)

    signs = [random.randrange(2) for i in range(m)]
    order = [[-1, -1] for i in range(m)]

    start = unchecked(order)
    knotEdge = []
    
    while start != -1:
        a, b, c, d = crossings[start]
        if order[start][0] == -1:
            order[start][0] = 1
            prev = start
            nxt = c
            nechci = a
        else:
            order[start][1] = 1
            prev = start
            nxt = d
            nechci = b
        cnt = 0
        knotEdge.append([nechci, start])
        while [prev, nxt] != [nechci, start]:
            knotEdge.append([prev, nxt])
            a, b, c, d = crossings[nxt]
            ind = crossings[nxt].index(prev)
                
            if ind == 0:
                order[nxt][0] = 1
                newNxt = c
            elif ind == 1:
                order[nxt][1] = 1
                newNxt = d
            elif ind == 2:
                order[nxt][0] = 0
                newNxt = a
            elif ind == 3:
                order[nxt][1] = 0
                newNxt = b
            prev = nxt
            nxt = newNxt
            #print(knotEdge)

        start = unchecked(order)

    notPD = []

    #print(knotEdge)

    for i in range(m):
        a, b, c, d = crossings[i]
        stav = order[i]
        sign = signs[i]

        if stav == [1, 1]:
            if sign == 1:
                cross = [b, c, d, a]
            else:
                cross = [a, b, c, d]
        elif stav == [1, 0]:
            if sign == 1:
                cross = [a, b, c, d]
            else:
                cross = [d, a, b, c]
        elif stav == [0, 1]:
            if sign == 1:
                cross = [c, d, a, b]
            else:
                cross = [b, c, d, a]
        elif stav == [0, 0]:
            if sign == 1:
                cross = [d, a, b, c]
            else:
                cross = [c, d, a, b]
        else:
            print(stav)
        notPD.append(cross)


    #print("notPD")
    #print(notPD)
    
    PD = notPD
    
    for i in range(len(notPD)):
        for j in range(len(notPD[i])):
            if [notPD[i][j], i] in knotEdge:
                PD[i][j] = knotEdge.index([notPD[i][j], i] ) + 1
            else:
                PD[i][j] = knotEdge.index([i,notPD[i][j]] ) + 1

    print(PD)
    
    return PD       
            


def generator(n):
    p=randomPoints(n)
    print("p")
    print(p)
    #p=[[27, 418], [198, 414], [197, 240], [67, 392], [375, 11]]
    tr = triangulation(p)
    print("tr")
    G, H = triangToGraph(tr, p)
    print("H")
            
    c=graphToKnot(H)
    print(c)
    edges = makeEdges(H)
    
p=[[250, 517], [122, 644], [326, 207], [642, 486], [618, 510], [374, 166], [679, 252]]
tr = triangulation(p)
G, H = triangToGraph(tr, p)
edges = makeEdges(H)

# problem, kdyz ma vrchol deg 2 nebo 1
