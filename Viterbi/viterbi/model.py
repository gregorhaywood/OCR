"""
The module is used to create and train a model.
"""

import sys
import os
import csv

from viterbi.char import Char

class Model(object):


    def __init__(self, mode, fname=None):
        """Load a model from a file or create one from a codec.
        Mode can be "o" to open an existing model or "c" to create
        a new one.
        """
        self.fitted = False
        if mode=="o":
            self._openModel(fname)
        elif mode=="c":
            self._createModel()
        else:
            raise Exception("Mode \"" + mode + "\"not recognised.")

    def _createModel(self):
        """Create an untrained model."""
        package, _ = os.path.split(__file__)
        file = open(package + "/Data/codec.csv", "r")
        self.codec = {}
        for line in csv.reader(file, escapechar="\\"):
            c = line[0]
            states = map(lambda x: (0.5,int(x)), line[1:])
            self.codec[c] = Char(c, states)
        file.close()


    def _openModel(self, fname):
        """Open a previously trained model"""
        raise NotImplementedError("Opening models is not implemented.")


    def fit(self, line, img):
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
        return results

    def forwards(self, state, col):
        """Forwards probability calculator."""
        # it is not possible to reach state x without
        # x transitions, so state<=col
        if state>col: return 0.0

        # base case
        if col==0 and state<=0:
            return self.stateList[0].emission(self.img[col])

        if state<0:
            state = 0

        # probability previous col was different state times that state's
        # transition probability
        change = self.forwards(state-1,col-1)*self.stateList[state-1].trans
        # probability previous col was same state times this state's (ie,
        # the stateof both columns) non-transition probability
        same = self.forwards(state,col-1)*(1-self.stateList[state-1].trans)
        emit = self.stateList[state].emission(self.img[col])
        return (change+same)*emit


    def backwards(self, state, col):
        """Backwards probability calculator."""
        # it is not possible to reach state x without
        # x transitions, so n columns before the end must
        # be at most n states from the end state (in order to reach it)
        if len(self.stateList)-state>len(self.img)-col:
            return 0.0

        # base case: final column, final state
        if col==len(self.img)-1 and state>=len(self.stateList)-1:
            return self.stateList[len(self.stateList)-1].emission(self.img[col])

        if col>=len(self.img):
            raise ValueError()

        if state>=len(self.stateList):
            state = len(self.stateList)-1


        # probability next col is different state times this state's
        # transition probability (likelyhood of changing into it)
        changeState = self.backwards(state+1,col+1)*self.stateList[state].trans

        # probability next col is same state times this state's
        # non-transition probability
        sameState = self.backwards(state,col+1)*(1-self.stateList[state].trans)
        emit = self.stateList[state].emission(self.img[col])
        return (changeState+sameState)*emit

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
