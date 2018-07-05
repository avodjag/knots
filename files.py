import ast
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

def do():
    PDs = []
    f = open("TorusKnots.rdf", 'r')
    for line in f:
        l = line.split()
        if '<invariant:PD_Presentation>' in l:
            #print(l)
            PD = [l[0][6:-1]]
            l[2] = l[2][1:]
            l[-2] = l[-2][:-1]
            #print(l[2:-1])
            for cr in l[2:-1]:
                spl = cr[6: -6]
                spl = spl.split(',')
                #print(spl)
                if len(spl) == 1:
                    tmp = spl[0]
                    spl = []
                    for i in range(4):
                        spl.append(int(tmp[i]))
                else:
                    for i in range(4):
                        spl[i] = int(spl[i])
                PD.append(spl)
            PDs.append(PD)
    return PDs

def safe(tr):
    for i in tr:
        f = open("./torus/" + i[0] + '.txt', 'w')
        f.write(str(i[1:]))
        f.close()

def data():
    data = open("knotData.txt", 'r')
    count = [0 for i in range(13)]
    for line in data:
        if line == 'PDNotation\n':
            continue
        PD = ast.literal_eval(line)
        l = len(PD)
        f = open("./uzly/table/" + str(l) + "_" + str(count[l]) + ".txt", 'w')
        f.write(line)
        f.close()
        count[l] = count[l] + 1
    data.close()
