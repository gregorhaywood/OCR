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

    def _makeRandom(self):

        # for simplicity
        chars = " &,-.:ABCDEFGHILMNOPQRSTVabcdefghilmnopp̃qq̃rstuvxyzãõĩũſṹẽ❧➽ꝑꝓꝗꝯ"
        short = ",.:ſ\-fijl1"
        medium = "ABCDEFGHIJKLNOPQRSTUVXYZabcdeghkopqstuvxyz023456789ãõĩũṹẽ&p̃ꝑꝓꝗꝯq̃"
        longChar = "MWmnrw❧➽"

        rnd = Rnd()
        def rndTr(): return rnd.randrange(45,65)/100
        def rndMu(): return rnd.randrange(10,30,5)/10


        codec = {}
        for c in chars:
            if c == " ":
                codec[c] = Char(c, [(NegLog(0.5), 0)])
            elif c in longChar:
                states = []
                for i in range(6):
                    tr = rndTr()
                    mu = rndMu()
                    states.append((NegLog(tr),mu))
                states.append((NegLog(0.5),0))
                codec[c] = Char(c, states)
            elif c in medium:
                states = []
                for i in range(4):
                    tr = rndTr()
                    mu = rndMu()
                    states.append((NegLog(tr),mu))
                states.append((NegLog(0.5),0))
                codec[c] = Char(c, states)
            elif c in short:
                states = []
                for i in range(2):
                    tr = rndTr()
                    mu = rndMu()
                    states.append((NegLog(tr),mu))
                states.append((NegLog(0.5),0))
                codec[c] = Char(c, states)
        self.codec = codec

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
        """Get the states for a line transcription"""
        # TODO
        # use fname following ocropus convention
        self.stateList = StateList(self.codec, line, img)
        self.img = img
        return self.stateList.fit()

    def forwards(self):
        return self.stateList.forwards()

    def backwards(self):
        return self.stateList.backwards()

    def expected(self):
        return self.stateList.expected()

    def update(self):
        self.stateList.update()
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



Training
trans: expected probability of state transitions for a column, i
    The sum of probabilities of state transition for each possible state of the column
    For each state j, the probability is:
        forwards(i,j)*stateChanged(i)*backwards(i+1,j+1)

stay: expected probability of no state transition after column i
    Sum for all states, as above
    For each state j:
        forwards(i,j)*stateUnchanged(i)*backwards(i+1,j)



Training is more complex. It is not for each column, but for each state.
change:
For the state (a,k):
i is derived from a and k.
For each col, j:
    forward(i, j) * P(a, k, k+1) * backward(i[+1]?, j+1)

stay:
For (a,k) with derived i
    forward(i, j) [* P(a, k, k)]? * backward(i, j+1)

Sum of all paths consistent with observation

In both cases, sum for all j, and resetimate by:
change/(change+stay)
Normalisation cancels out, so is not needed.

(a,k) can coresponse to multiple states with different i. How should this be handled?
-mean
-handle seperatly, combine later

Are these formula correct?
Can stay be summed, as they are not exclusive possibilities?

For mu:
For (a,k)..i as above
For all j:
    E(a,k,i,j,n_i) = forward(i, j) * backward(i, j) [ / (emit(n_i)) due to implementation]
How does this give mu?

ln(n) for each count gives an estimate of mu. Multiply by probability given above,
sum, and divide by forward(total)?

Average of logs weighted by f/b probability



The -1 in the emit probability will cause problems and needs dealt with, either there,
or by adding 1 to counts here. It is delt with here, else log(0) would cause errors



"""
