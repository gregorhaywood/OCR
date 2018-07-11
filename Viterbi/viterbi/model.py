"""
The module is used to create and train a model.
"""

import sys
import os
import csv
from functools import reduce

from viterbi.char import Char
from math import log, exp
import sys


ZERO = sys.float_info[0]
PREC = -log(sys.float_info[3])-log(3)
def to(x):
    if x>0:
        return -log(x)
    else:
        return ZERO

def fr(x):
    return exp(-x)

def mult(a,b):
    if a == ZERO or b == ZERO:
        return ZERO
    else:
        return a+b

def add(a,b):
    # handle zero
    if a == ZERO:
        return b
    if b == ZERO:
        return a
    # handle extremes
    if a-b > PREC:
        return b
    if b-a > PREC:
        return a
    # normal
    c = min(a,b)
    return -log(exp(-a+c)+exp(-b+c))+c


class Model(object):


    def __init__(self, mode, fname=None):
        """Load a model from a file or create one from a codec.
        Mode can be "o" to open an existing model or "c" to create
        a new one.
        """
        self.forward = []
        self.backward = []
        if mode=="o":
            self._openModel(fname)
        elif mode=="c":
            package, _ = os.path.split(__file__)
            fname = package + "/data/codec.csv"
            self._openModel(fname)
        else:
            raise Exception("Mode \"" + mode + "\"not recognised.")

    def _openModel(self, fname):
        """Create an untrained model."""
        package, _ = os.path.split(__file__)
        file = open(package + "/data/codec.csv", "r")
        self.codec = {}
        for line in csv.reader(file):
            c = line[0]
            states = []
            for i in range(1,len(line),2):
                states.append((float(line[i]),float(line[i+1])))
            self.codec[c] = Char(c, states)
        file.close()

    def storeModel(self, fname):
        """Store a model for future use"""
        file = open(fname, "w")
        writer = csv.writer(file)
        for char in self.codec.values():
            name, data = char.store()
            row = [name] + list(reduce(lambda x, y: x+y, data))
            writer.writerow(row)
        file.close()

    def fit(self, line, img, fb=False):
        """Get the states for a line transcription"""
        class Start(object):
            def __init__(self):
                self.next = True
        start = Start()

        previous = self.codec[line[0]].getStates(start)
        for c in line[1:]:
            previous = self.codec[c].getStates(previous)
        results = start.next.fit(img)
        self.stateList = start.next.toList()
        self.img = img
        self.forward = []
        self.backward = []
        if fb:
            self.forwards()
            self.backwards()
        return results

    def forwards(self):
        if self.forward != []:
            return self.forward

        # col  can only be on state
        forward = []
        forward.append([to(self.stateList[0].emission(self.img[0]))]
                    + [to(0)]*(len(self.stateList)-1))
        # other cols
        for col in range(1,len(self.img)):
            # state is at most col
            colList = []
            for state in range(col+1):
                try:
                    em = (self.stateList[state].emission(self.img[col]))
                except IndexError:
                    continue
                change = to(0)
                if state > 0:
                    change = mult(forward[col-1][state-1],to(self.stateList[state-1].getTrans()))
                same = to(0)
                # col-1 might not have an entry for state
                try:
                    same = mult(forward[col-1][state],to(self.stateList[state-1].getStay()))
                except IndexError:
                    pass
                colList.append(mult(add(change,same),em))
            colList = colList + ([to(0)]*(len(self.stateList)-len(colList)))
            forward.append(colList)
        self.forward = forward
        return self.forward

    def backwards(self):
        if self.backward != []:
            return self.backward
        backward = [[]]*len(self.img)

        # col  can only be on state
        backward[-1] = [0]*(len(self.stateList)-1) + [(self.stateList[-1].emission(self.img[-1]))]

        # other cols
        for col in range(len(self.img)-2,-1,-1):
            # state is at most col
            colList = []
            start = len(self.stateList)-1
            end = start - (len(self.img)-col)-1
            for state in range(start ,end,-1):
                if (state < 0):
                    break
                em = (self.stateList[state].emission(self.img[col]))
                change = 0
                # state index may be out of bounds
                try:
                    change = backward[col+1][state+1]*self.stateList[state].getTrans()
                except IndexError:
                    pass
                same = 0
                try:
                    same = backward[col+1][state]*self.stateList[state].getStay()
                except IndexError:
                    pass
                colList.insert(0, ((change+same)*em))
            colList = [0]*(len(self.stateList)-len(colList)) + colList
            backward[col] = colList
        self.backward = backward
        return self.backward

    def expected(self):
        """For training."""
        # i: state
        # j: col
        # forward(i, j) * P(a, k, k+1) * backward(i[+1], j+1)
        if self.forward == []:
            self.forwards()
        if self.backward == []:
            self.backwards()
        change = []
        for col in range(len(self.img)):
            e = 0
            for state in range(len(self.stateList)):
                f = self.forward[col][state]
                try:
                    b = self.backward[col+1][state+1]
                except IndexError:
                    # no transition past last state or col
                    continue
                # normalise
                # balance scaling
                # scaling gets too complex
                # use alternative representation

                lim = 1000000
                if f > lim: f = lim
                if b > lim: b = lim
                t = self.stateList[state].getTrans()
                e = e + f*b*t
                """
                print("F:\t{0}".format(f))
                print("B:\t{0}".format(b))
                print("T:\t{0}".format(t))
                print("F.B.T:\t{0}".format(f*b*t))
                print("E:\t{0}".format(e))
                print()
                """
            change.append(e)
        return change
"""
backward(L, M) = P(a,k,n_M)
where a is the last letter in the transcription, with k states.

backward(i, j) = [
        backward(i+1, j+1) * P(a, k, k+1) +
            probability next col is next state going back times
            forwards transition probability
        backward(i, j+1) * P(a, k, k) ] *
            probability next col is same state going back
		P(a,k,n_{j})


        the probability of going back to this column and being in this state
"""



"""

    forward(i, j+1) = [ forward(i-1, j) * P(a', k', k) + forward(i, j) * P(a, k, k) ] *
						P(a,k,n_{j+1})
    so
    forward(i,j) = [
        forward(i-1, j-1) * P(a', k', k)
            the forward probability of the previous column being in the previous state
            times the transision probability from the previous state
        + forward(i, j-1) * P(a, k, k) ]
            f.p. of previous column being same state times the non-transision probability
            for that state
        * P(a,k,n_{j})
            all times emission probability for this state for this column

        so:
            the probability of getting to this state and column (i.e., the sum
            of the probabilities of the two routes) times the emission probability
        so:
            the probability of advancing to this column and being in this state


Let the columns of the lines (i.e. the numbers of pixels in these columns)
be n_1 ... n_M. Then in principle (if we exclude optimisations), we need to
compute values forward(i,j) and backward(i,j), where 1 <= i <= L and 1 <= j <= M.

forward(1, 1) = P(a,1,n_1)
where a is the first letter in the transcription.

forward(i, j+1) = [ forward(i-1, j) * P(a', k', k) + forward(i, j) * P(a, k, k) ] *
						P(a,k,n_{j+1})
where state i corresponds to state k for letter a, and a'=a and k'=k-1 if
k > 1 and a' is the previous letter, say b, and k' is the final state for b.

state i is state k of letter a

if k>1:
    a'=a
    k'=k-1
else:
    a' = previous letter
    k' = final state of a'
"""
