from math import *

def addLog(filename, druhe):
    out = open(druhe, "w")
    f = open(filename, "r")

    for line in f:
        l = line.split()
        out.write(l[1] + " " + l[2] + " ")
        c = log2(float(l[2]))
        out.write(str(c))
        out.write("\n")
    f.close()
    out.close()

def mean(filename, druhe):
    out = open("meansB.dat", "w")
    f = open(filename, "r")
    a = [0 for i in range(13)]
    c = [0 for i in range(13)]
    for line in f:
        l = line.split()
        j = int(l[1])
        a[j] = a[j] + float(l[2])
        c[j] = c[j] + 1
    f.close()
    
    for i in range(13):
        if c[i] != 0:
            out.write(str(i) + " " + str(a[i]/c[i]))
            out.write("\n")
    out.close()
