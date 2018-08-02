"""
The module is used to create and train a model.
"""

import sys
import os
import csv
from functools import reduce
from math import log, exp
from random import Random as Rnd

from viterbi.char import Char
from viterbi.negLog import NegLog
from viterbi.stateList import StateList


class Model(object):

    def __init__(self, mode, fname=None):
        """Load a model from a file or create one from a codec.
        Mode can be "o" to open an existing model or "c" to create
        a new one.
        """
        if mode=="o":
            self._openModel(fname)
        elif mode=="c":
            package, _ = os.path.split(__file__)
            fname = package + "/data/codec.csv"
            self._openModel(fname)
        elif mode=="r":
            self._makeRandom()
        else:
            raise Exception("Mode \"" + mode + "\"not recognised.")

    def _openModel(self, fname):
        """Open an model."""
        file = open(fname,"r")
        self.codec = {}
        for line in csv.reader(file):
            c = line[0]
            states = []
            for i in range(1,len(line),2):
                states.append((NegLog(negLog=float(line[i])),float(line[i+1])))
            self.codec[c] = Char(c, states)
        file.close()

    def store(self, fname):
        """Store a model for future use"""
        file = open(fname, "w")
        writer = csv.writer(file)
        for char in self.codec.values():
            name, data = char.store()
            row = [name] + list(reduce(lambda x, y: x+y, data))
            writer.writerow(row)
        file.close()
        
    def fit(self, line, img):
        """Fit the model to the input."""
        stateList = StateList(self.codec, line, img)
        return stateList.fit()

    def train(self, line, img):
        """Train the model on the input."""
        stateList = StateList(self.codec, line, img)
        stateList.train()


