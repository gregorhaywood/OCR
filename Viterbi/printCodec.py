


import sys
import csv
from viterbi.negLog import NegLog


with open(sys.argv[1],"r") as file:
    for line in csv.reader(file):
        c = line[0]
        print("{0}:".format(c))
        states = []
        for i in range(1,len(line),2):
            t = NegLog(negLog=float(line[i])).prob()
            m = float(line[i+1])
            print("{0}\t\t{1}".format(t,m))
