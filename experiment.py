from jones import *
from os import listdir
import time
import ast

table = "uzly/table/"
alt = "uzly/alt_knots/"
knots = "uzly/knots/"
links = "uzly/links/"
torus = "uzly/torus/"

#direc ve formatu uzly/fsdf/
def measure(direc, var='A'):
    log = open("./uzly/logs/" + direc[5:-1] +  "_log_" + var + ".txt", "w")
    log.close()
    a = listdir(direc)
    files = sorted(a)
    for filename in files:
        #print(filename)
        data = open(direc + filename, "r")
        
        PD = data.readline()
        PD = ast.literal_eval(PD)

        start = time.time()
        jones(PD, var)
        end = time.time()

        elapsed = end-start
        #print(elapsed)
        l = len(PD)
        log = open("./uzly/logs/" + direc[5:-1] +  "_log_" + var + ".txt", "a")
        log.write(filename + " " + str(l) + " " + str(elapsed) + "\n")
        data.close()
        log.close()

# da uzly velikosti m az n-1       
def measure2(direc, m, n, var='A'):
    log = open("./uzly/logs/" + direc[5:-1] +  "_log_" + var + "_" + str(m) + "_" + str(n-1) + "_" + ".txt", "a+")
    log.close()
    files = [(str(i) + ".txt") for i in range(m, n)]
    for filename in files:
        #print(filename)
        data = open(direc + filename, "r")
        
        PD = data.readline()
        PD = ast.literal_eval(PD)

        start = time.time()
        jones(PD, var)
        end = time.time()

        elapsed = end-start
        #print(elapsed)
        l = len(PD)
        log = open("./uzly/logs/" + direc[5:-1] +  "_log_" + var + "_" +str(m) + "_" + str(n-1) + "_" + ".txt", "a")
        log.write(filename + " " + str(l) + " " + str(elapsed) + "\n")
        data.close()
        log.close()
        
def do():
    #measure(table, 'A')
    #print("table A")
    #measure(table, 'B')
    #print("table B")
    #measure(table, 'R')
    #print("table c")

    #measure(torus, 'A')
    #print("a")
    #measure(torus, 'B')
    #print("b")
    #measure(torus, 'R')
    #print("c")

    #measure2(knots, 13, 50, 'A')
    #print("a")
    #measure2(knots, 13, 35, 'B')
    #print("b")
    #measure2(knots, 13, 20, 'R')
    #print("c")

    #measure2(alt, 13, 40, 'A')
    #print("a")
    #measure2(alt, 13, 35, 'B')
    #print("b")
    #measure2(alt, 13, 20, 'R')
    #print("c")

    #measure2(links, 13, 40, 'A')
    #print("a")
    #measure2(links, 13, 35, 'B')
    #print("b")
    #measure2(links, 13, 20, 'R')
    #print("c")

    measure2(knots, 35, 40, 'B')
    measure2(alt, 35, 40, 'B')
    measure2(links, 35, 40, 'B')

    measure2(knots, 40, 45, 'B')
    measure2(alt, 40, 45, 'B')
    measure2(links, 40, 45, 'B')

    measure2(knots, 45, 50, 'B')
    measure2(alt, 45, 50, 'B')
    measure2(links, 45, 50, 'B')
    
    print("alllllll")
    
