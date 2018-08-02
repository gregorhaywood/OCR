


from matplotlib.image import imread
import numpy as np


import csv
from viterbi.negLog import NegLog


_DIVIDE = 30
def openImg(path):
    """
    Open an image, and return an array of counts of black 
    pixels in each column. Also trims white space and noise 
    at then begining and and end of the line.
    """
    img = np.array(imread(path))
    counts = list(map(lambda x: len(img)-x.sum(), img.transpose()))
    
    # trim start and end
    start = 0
    while (counts[start] == 0): start += 1
    buf = start
    while (counts[buf] != 0): buf += 1
    white = buf
    while (counts[white] == 0): white += 1
    if white-buf > _DIVIDE:
        start = white

    end = len(counts)
    while (counts[end-1] == 0): end -= 1
    buf = end
    while (counts[buf-1] != 0): buf -= 1
    white = buf
    while (counts[white-1] == 0): white -= 1
    if buf-white > _DIVIDE:
        end = white
        
    return start, end, counts[start:end]
    

def printCodec(fname):
    with open(fname, "r") as file:
        for line in csv.reader(file):
            c = line[0]
            print("{0}:".format(c))
            states = []
            for i in range(1,len(line),2):
                t = NegLog(negLog=float(line[i])).prob()
                m = float(line[i+1])
                print("{0}\t\t{1}".format(t,m))