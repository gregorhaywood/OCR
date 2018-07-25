from matplotlib.image import imread, imsave
import numpy as np
from viterbi.char import Char
from viterbi.model import Model
from functools import reduce

import os
import glob
import sys


import csv

DIVIDE = 30

BLACK = [0.0,0.0,0.0,1.0]
WHITE = [1.0,1.0,1.0,1.0]
RED = [1.0,0.0,0.0,1.0]
GREEN = [0.0,1.0,0.0,1.0]
BLUE = [0.0,0.0,1.0,1.0]
CYAN = [0.0,1.0,1.0,1.0]
MAGENTA = [1.0,0.0,1.0,1.0]
YELLOW = [1.0,1.0,0.0,1.0]



# Return True for BLACK cells
def isChar(x):
    if x==0:
        return True
    else:
        return False

def trainOn(model, path):
    dr, fname = os.path.split(path)
    
    # transcription
    with open(path + ".gt.txt") as f:
        line = f.read()[:-1]
    if len(line) == 0:
        return

    # image
    img = np.array(imread(path + ".bin.png"))
    counts = list(map(lambda x: len(img)-x.sum(), img.transpose()))
    start = 0
    while (counts[start] == 0): start += 1
    buf = start
    while (counts[buf] != 0): buf += 1
    white = buf
    while (counts[white] == 0): white += 1
    if white-buf > DIVIDE:
        start = white
    
    end = len(counts)
    while (counts[end-1] == 0): end -= 1
    buf = end
    while (counts[buf-1] != 0): buf -= 1
    white = buf
    while (counts[white-1] == 0): white -= 1
    if buf-white > DIVIDE:
        end = white
    m.fit(line, counts[start:end], fit=False)
    m.expected()
    m.update()
    results, p = m.fit(line, counts[start:end])
    
    m.store("Results/" + path + ".csv")

    def c(col):
        if str(results[col])[0] ==  " ":
            return WHITE
        v = int(str(results[col])[1])
        if v == 0:
            return MAGENTA
        v = v%5
        if v == 0:
            return CYAN
        if v == 1:
            return GREEN
        if v == 2:
            return BLUE
        if v == 3:
            return YELLOW
        if v == 4:
            return RED
        return None

    trans = img.transpose()
    output = []
    for col in range(start):
        output.append([WHITE]*len(img))
    for col in range(len(results)):
        val = 1-trans[col+start].sum()/len(img)
        output.append(list(map(
            lambda x: BLACK if isChar(x) else c(col),
            trans[col+start])))

    for i in range(len(output)):
        if i%50==0:
            output[i][-1] = BLACK
            output[i][-2] = BLACK

        if i%100==0:
            output[i][-3] = BLACK
            output[i][-4] = BLACK
    fn = "Results/" + path + ".png"
    out = np.array(output).transpose(1,0,2)
    imsave(fn, out, format="png")
    print("Trained on {0}".format(path))







m = Model( "c")

if len(sys.argv) > 1:
    # fit for argv
    os.chdir("Training")
    file = sys.argv[1][9:]
    trainOn(m, file)
else:
    os.chdir("Training")
    for i in range(1,7):
        print("Page:\t{0}".format(i))
        files = glob.glob("000{0}/0001/*.txt".format(i))
        files.sort()
        for file in files:
            trainOn(m, file.split(".")[0])

# TODO - general
# readability/maintainability/documentation
#

# TODO
# MAYBE:
# setting state number:
    # merge states that have similar mu
        # (ie, e1(n)*stay > e2(n)*stay for most reasonabe n
    # split states that have diverse emission probabilities


# TODO enhancments
# parallel forwards/backwards/training
# non-binary image version


























#end
