


from matplotlib.image import imread, imsave
import numpy as np


import csv
from viterbi.negLog import NegLog


_DIVIDE = 30
_BLACK = [0.0,0.0,0.0,1.0]
_WHITE = [1.0,1.0,1.0,1.0]
_RED = [1.0,0.0,0.0,1.0]
_GREEN = [0.0,1.0,0.0,1.0]
_BLUE = [0.0,0.0,1.0,1.0]
_CYAN = [0.0,1.0,1.0,1.0]
_MAGENTA = [1.0,0.0,1.0,1.0]
_YELLOW = [1.0,1.0,0.0,1.0]

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
    

def saveImg(states, start, imgPath, path, allColours=False):
    """Store img at path coloured according to states"""
    def colour(pixel, col):
        if pixel == 0:
            return _BLACK
        elif allColours:
            if str(states[col])[0] ==  " ":
                return _WHITE
            v = int(str(states[col])[1])
            if v == 0:
                return _MAGENTA
            v = v%5
            if v == 0:
                return _CYAN
            if v == 1:
                return _GREEN
            if v == 2:
                return _BLUE
            if v == 3:
                return _YELLOW
            if v == 4:
                return _RED
        else:
            if str(states[col])[0] ==  " ":
                return _RED 
            else: 
                return _WHITE
    
    img = np.array(imread(imgPath))
    counts = list(map(lambda x: len(img)-x.sum(), img.transpose()))
    
    # trim start
    start = 0
    while (counts[start] == 0): start += 1
    buf = start
    while (counts[buf] != 0): buf += 1
    white = buf
    while (counts[white] == 0): white += 1
    if white-buf > _DIVIDE:
        start = white

    trans = img.transpose()
    
    output = [[_WHITE]*len(img)] * start
    for col in range(len(states)):
        output.append(list(
                map(lambda x: colour(x, col),
                    trans[col+start])
            ))
            
    out = np.array(output).transpose(1,0,2)
    imsave(path, out, format="png")



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