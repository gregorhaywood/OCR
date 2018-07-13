"""
The module is used to create and train a model.
"""

import sys
import os
import csv
from functools import reduce

from viterbi.char import Char
from math import log, exp
from viterbi.negLog import NegLog


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
        forward.append([(self.stateList[0].emission(self.img[0]))]
                    + [NegLog(0)]*(len(self.stateList)-1))
        # other cols
        for col in range(1,len(self.img)):
            # state is at most col
            colList = []
            for state in range(col+1):
                try:
                    em = self.stateList[state].emission(self.img[col])
                except IndexError:
                    continue
                change = NegLog(0)
                if state > 0:
                    change = forward[col-1][state-1] * self.stateList[state-1].getTrans()
                same = NegLog(0)
                # col-1 might not have an entry for state
                try:
                    same = forward[col-1][state] * self.stateList[state-1].getStay()
                except IndexError:
                    pass
                colList.append((change+same) * em)
            colList = colList + ([NegLog(0)]*(len(self.stateList)-len(colList)))
            forward.append(colList)
        self.forward = forward
        return self.forward

    def backwards(self):
        if self.backward != []:
            return self.backward
        backward = [[]]*len(self.img)

        # col  can only be on state
        backward[-1] = [NegLog(0)]*(len(self.stateList)-1) + [self.stateList[-1].emission(self.img[-1])]

        # other cols
        for col in range(len(self.img)-2,-1,-1):
            # state is at most col
            colList = []
            start = len(self.stateList)-1
            end = start - (len(self.img)-col)-1
            for state in range(start ,end,-1):
                if (state < 0):
                    break
                em = self.stateList[state].emission(self.img[col])
                change = NegLog(0)
                # state index may be out of bounds
                try:
                    change = backward[col+1][state+1]*self.stateList[state].getTrans()
                except IndexError:
                    pass
                same = NegLog(0)
                try:
                    same = backward[col+1][state]*self.stateList[state].getStay()
                except IndexError:
                    pass
                colList.insert(0, ((change+same)*em))
            colList = [NegLog(0)]*(len(self.stateList)-len(colList)) + colList
            backward[col] = colList
        self.backward = backward
        return self.backward

    def expected(self):
        """Probability of a transition occuring after a column."""
        if self.forward == []:
            self.forwards()
        if self.backward == []:
            self.backwards()

        """
        change = []
        # for every image column
        for col in range(len(self.img)):
            e = NegLog(0)
            # for every possible state
            for state in range(len(self.stateList)):
                f = self.forward[col][state]
                try:
                    b = self.backward[col+1][state+1]
                except IndexError:
                    # no transition past last state or col
                    continue

                t = self.stateList[state].getTrans()
                e = e + f*b*t
            change.append(e)
        """
        # updated to state version
        change = []
        for state in range(len(self.stateList)):
            e = NegLog(0)
            for col in range(len(self.img)):
                f = self.forward[col][state]
                try:
                    b = self.backward[col+1][state+1]
                except IndexError:
                    # no transition past last state or col
                    continue
                t = self.stateList[state].getTrans()
                e = e + f*b*t
            change.append(e)

        """
        stay = []
        # for every image column
        for col in range(len(self.img)):
            e = NegLog(0)
            # for every possible state
            for state in range(len(self.stateList)):
                f = self.forward[col][state]
                try:
                    b = self.backward[col+1][state]
                except IndexError:
                    # no transition past last state or col
                    continue

                t = self.stateList[state].getStay()
                e = e + f*b*t
            stay.append(e)
        """

        # updated to state version
        stay = []
        for state in range(len(self.stateList)):
            e = NegLog(0)
            for col in range(len(self.img)):
                f = self.forward[col][state]
                try:
                    b = self.backward[col+1][state]
                except IndexError:
                    # no transition past last state or col
                    continue
                t = self.stateList[state].getStay()
                e = e + f*b*t
            stay.append(e)

        update = []
        for i in range(len(change)-1):
            update.append(change[i]/(change[i]+stay[i]))
        return update


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



"""
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
or by adding 1 to counts here.



"""
