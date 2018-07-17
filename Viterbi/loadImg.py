from matplotlib.image import imread, imsave
import numpy as np
from hmmlearn import hmm
from viterbi.char import Char
from viterbi.model import Model
from functools import reduce




black = [0.0,0.0,0.0,1.0]
white = [1.0,1.0,1.0,1.0]
red = [1.0,0.0,0.0,1.0]
green = [0.0,1.0,0.0,1.0]
blue = [0.0,0.0,1.0,1.0]
cyan = [0.0,1.0,1.0,1.0]
magenta = [1.0,0.0,1.0,1.0]
yellow = [1.0,1.0,0.0,1.0]



# Return True for black cells
def isChar(x):
    if x==0:
        return True
    else:
        return False

def makeHeatMap(fname):
    img = np.array(imread(fname))

    output =[]
    for col in img.transpose():
        val = 1-col.sum()/len(img)
        output.append(list(map(
            lambda x: black if isChar(x) else [1.0,0.0,0.0,val],
            col)))

    imsave("Data/heat.png", np.array(output).transpose(1,0,2), format="png")


def runHMM(fname):
    img = np.array(imread(fname))
    counts = list(map(lambda x: [len(img)-x.sum()], img.transpose()))
    print(counts)
    return
    vals = 6
    model = hmm.GaussianHMM(n_components=vals, n_iter=100, init_params="mcs")
    base= 0.5
    arr = []
    for i in range(vals):
        r = []
        for j in range(vals):
            if i==j:
                r.append(base)
            else:
                r.append((1-base)/(vals-1))
        arr.append(r)
    model.transmat_ = np.array(arr)

    model.fit(counts)
    results = model.predict(counts)

    output =[]
    trans = img.transpose()

    def c(col):
        v = results[col]%6
        if v == 0:
            return red
        if v == 1:
            return green
        if v == 2:
            return blue
        if v == 3:
            return yellow
        if v == 4:
            return cyan
        else:
            return magenta

    for col in range(len(trans)):
        val = 1-trans[col].sum()/len(img)
        output.append(list(map(
            lambda x: [0.0,0.0,0.0,1.0] if isChar(x) else c(col),
            trans[col])))

    imsave("Data/results.png", np.array(output).transpose(1,0,2), format="png")

def myModel(fname):

    img = np.array(imread(fname))
    counts = list(map(lambda x: len(img)-x.sum(), img.transpose()))
    start = 0
    while (counts[start] == 0): start = start + 1
    end = len(counts)
    while (counts[end-1] == 0): end = end - 1
    m = Model( "c", "Data/codec")
    results = m.fit("ie vous mon⌠treray le⌠pou⌠e la femme a laignel, & me mena en", counts[start:end])

    def c(col):
        if results[col][0] ==  " ":
            return white
        v = int(results[col][1])
        if v == 0:
            return magenta
        v = v%5
        if v == 0:
            return cyan
        if v == 1:
            return green
        if v == 2:
            return blue
        if v == 3:
            return yellow
        if v == 4:
            return red
        return None

    trans = img.transpose()
    output = []
    for col in range(start):
        output.append([white]*len(img))
    for col in range(len(results)):
        val = 1-trans[col+start].sum()/len(img)
        output.append(list(map(
            lambda x: black if isChar(x) else c(col),
            trans[col+start])))

    for i in range(len(output)):
        if i%50==0:
            output[i][-1] = black
            output[i][-2] = black

        if i%100==0:
            output[i][-3] = black
            output[i][-4] = black

    # mark mean
    """
    trans = img.transpose()
    m = len(img)/2
    for col in range(len(output)):
        bl = []
        for i in range(len(trans[col])):
            if isChar(trans[col][i]):
                bl.append(i)
        m2 = m
        if len(bl)>0:
            m2 = reduce(lambda x,y: x+y, bl)/len(bl)
        m = (30*m+m2+len(img)/2)/32
        output[col][int(m)] = red
    """
    imsave("Data/model.png", np.array(output).transpose(1,0,2), format="png")


def testProb(fname, startState=0, startCol=0):
    img = np.array(imread(fname))
    counts = list(map(lambda x: len(img)-x.sum(), img.transpose()))
    start = 0
    while (counts[start] == 0): start = start + 1

    m = Model( "c", "Data/codec")
    results = m.fit("ie vous mon⌠treray le⌠pou⌠e la femme a laignel, & me mena en", counts[start:])

    for col in range(start+startCol, start+startCol+5):
        for state in range(startState, startState+3):
            print("({0},{1}):\t{2}:\t{3}".format(state,col,counts[col],m.forwards(state,col)))




fname = "Data/img.png"
# makeHeatMap(fname)
# runHMM(fname)
# testProb(fname,2,6)
# myModel(fname)

# print("done")

import csv


img = np.array(imread(fname))
counts = list(map(lambda x: len(img)-x.sum(), img.transpose()))
start = 0
while (counts[start] == 0): start = start + 1

end = len(counts)
while (counts[end-1] == 0): end = end - 1

m = Model( "c")

results = m.fit("ie vous mon⌠treray le⌠pou⌠e la femme a laignel, & me mena en", counts[start:end])


"""
e = m.expected()
for i in range(len(e)):
    print("{0}:\t{1}".format(m.stateList[i], e[i].prob()))
"""

bw = m.backwards()
fw = m.forwards()

file = open("forwards.csv", "w")
writer = csv.writer(file)
for col in fw: # image col, not array col
    writer.writerow(col)
file.close()

file = open("backwards.csv", "w")
writer = csv.writer(file)
for col in bw: # image col, not array col
    writer.writerow(col)
file.close()

"""
for i in range(len(fw)):
    #print("{0}:\t{1}".format(i, fw[i][0]))
    if reduce(lambda x,y: x and (y.isZero()), fw[i], True):
        print("Forward ends:\t{0}".format(i))
        break


for i in range(len(bw)-1,0,-1):
    #print("{0}:\t{1}".format(i, bw[i][0]))
    if reduce(lambda x,y: x and (y.isZero()), bw[i], True):
        print("Backwards ends:\t{0}".format(i))
        break
"""
# TODO
# log version of other training functions
# heat map of probabilities (to show likely wrong values and visualise training)
# training































#end
