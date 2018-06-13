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

def triangulation(points):
    hull = convexHull(points)
    triang = triangPoly(hull)
    for P in points:
        if P in hull:
            continue
        for tr in triang:
            if inTriangle(tr, P):
                break
        

# na primce proste nechavam, bo by s tim slo pohnout, ackoli tam budou dvojite hrany
# po smeru rucicek
def convexHull(points):
    if len(points) < 4:
        print("Kratke")
        return
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

# po smeru, [0, i, i+1]
def triangPoly(polygon):
    n = len(polygon)
    triang = []
    for i in range(1, n-1):
        triang.append([polygon[0], polygon[i], polygon[i+1]])
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
