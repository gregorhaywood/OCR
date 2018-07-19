from matplotlib.image import imread, imsave
import numpy as np
from hmmlearn import hmm
from viterbi.char import Char
from viterbi.model import Model
from functools import reduce

import os
import glob
import sys




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
    m = Model( "c")

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



def storeImg(m, img, fname):
    #img = np.array(imread(fname))
    counts = list(map(lambda x: len(img)-x.sum(), img.transpose()))
    start = 0
    while (counts[start] == 0): start = start + 1
    end = len(counts)
    while (counts[end-1] == 0): end = end - 1
    #m = Model( "c", "Data/codec")
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

    imsave(fname, np.array(output).transpose(1,0,2), format="png")




def trainOn(model, path):
    dr, fname = os.path.split(path)

    img = np.array(imread(path + ".bin.png"))
    counts = list(map(lambda x: len(img)-x.sum(), img.transpose()))
    start = 0
    while (counts[start] == 0): start = start + 1
    end = len(counts)
    while (counts[end-1] == 0): end = end - 1

    with open(path + ".gt.txt") as f:
        line = f.read()[:-1]
    if len(line) == 0:
        return

    results = m.fit(line, counts[start:end])
    m.expected()
    m.update()

    m.store("Results/" + path + ".csv")

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

    imsave("Results/" + path + ".png", np.array(output).transpose(1,0,2), format="png")
    #storeImg(m,img,"Results/" + path + ".png")
    print("Trained on {0}".format(path))


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

m = Model( "r")

os.chdir("Training")
for i in range(1,7):
    print("Page:\t{0}".format(i))
    files = glob.glob("000{0}/0001/*.txt".format(i))
    files.sort()
    for file in files:
        trainOn(m, file.split(".")[0])
os.chdir("..")
sys.exit(0)

stepSize = 2

results = m.fit("ie vous monſtreray leſpouſe la femme a laignel, & me mena en", counts[start:end])
storeImg(m,img,"Data/model.png")

#sys.exit(0)

for i in range(stepSize):
    m.expected()
    m.update()

m.store("codex2")
storeImg(m,img,"Data/model2.png")
print("Training 1 Done")

for i in range(stepSize):
    m.expected()
    m.update()
m.store("codex3")
storeImg(m,img,"Data/model3.png")
print("Training 2 Done")

for i in range(stepSize):
    m.expected()
    m.update()
m.store("codex4")
storeImg(m,img,"Data/model4.png")

# TODO - general
# readability/maintainability/documentation
#

#TODO -today
# random start - done
# training infrastructure - done
#

# TODO - avoid min/max
# random strart codex
# mass data training infrastructure
# just increase transition probability for states that appear lots
# MAYBE:
# setting state number:
    # merge states that have similar mu
        # (ie, e1(n)*stay > e2(n)*stay for most reasonabe n
    # split states that have diverse emission probabilities

# TODO enhancments
# parallel forwards/backwards/training
# trimming unwanted black marks
# non-binary image version


























#end
