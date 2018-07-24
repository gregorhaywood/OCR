


from math import sqrt, pi, exp, log


from matplotlib.image import imread, imsave
import numpy as np
from viterbi.model import Model
from functools import reduce

import os
import glob
import sys







img = np.array(imread(sys.argv[1] + ".bin.png"))
counts = list(map(lambda x: len(img)-x.sum(), img.transpose()))
start = 0
while (counts[start] == 0): start = start + 1
end = len(counts)
while (counts[end-1] == 0): end = end - 1

m = Model( "c")

with open(sys.argv[1] + ".gt.txt") as f:
    line = f.read()[:-1]

results = m.fit(line, counts[start:end])

for i in range(len(results)):
    print("{0}:\t{1}".format(results[i], log(counts[i+start] + 1)))