def fileToPD(filename):
    PDknot = []
    f = open(filename, 'r')
    for line in f:
        cross = line.split()
        if cross != []:
            for i in range(4):
                cross[i] = int(cross[i])
        PDknot.append(cross)
    return PDknot
