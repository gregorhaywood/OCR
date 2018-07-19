

"""
Store a model's states as referances to characters
"""

from functools import reduce
from viterbi.negLog import NegLog
from math import log

class StateList(object):

    def __init__(self, codec, string, img):
        # gets order of states
        self.chars = []
        for c in string:
            self.chars.append(codec[c])
        self.img = img

        self.states = []
        for c in self.chars:
            self.states += c.states

    def fit(self):
        # fit
        index = 0
        self.fitted = []
        for col in self.img:
            # get state
            current = self[index]
            try:
                nextState = self[index  + 1]
            except IndexError:
                self.fitted.append(str(current))
                continue

            # store
            if current.getEmission(col) * current.getStay() > nextState.getEmission(col) * current.getTrans():
                self.fitted.append(str(current))
            else:
                self.fitted.append(str(nextState))
                index += 1
        return self.fitted

    def backwards(self):
        backward = [[]]*len(self.img)

        # col  can only be on state
        backward[-1] = [NegLog(0)]*(len(self)-1) + [self[-1].getEmission(self.img[-1])]

        # other cols
        for col in range(len(self.img)-2,-1,-1):
            # state is at most col
            colList = []
            start = len(self)-1
            end = start - (len(self.img)-col)-1
            for state in range(start ,end,-1):
                if (state < 0):
                    break
                em = self[state].getEmission(self.img[col])
                change = NegLog(0)
                # state index may be out of bounds
                try:
                    change = backward[col+1][state+1]*self[state].getTrans()
                except IndexError:
                    pass
                same = NegLog(0)
                try:
                    same = backward[col+1][state]*self[state].getStay()
                except IndexError:
                    pass
                colList.insert(0, ((change+same)*em))
            colList = [NegLog(0)]*(len(self)-len(colList)) + colList
            backward[col] = colList
        return backward

    def forwards(self):

        # col  can only be on state
        forward = []
        forward.append([(self[0].getEmission(self.img[0]))]
                    + [NegLog(0)]*(len(self)-1))
        # other cols
        for col in range(1,len(self.img)):
            # state is at most col
            colList = []
            for state in range(col+1):
                try:
                    em = self[state].getEmission(self.img[col])
                except IndexError:
                    continue
                change = NegLog(0)
                if state > 0:
                    change = forward[col-1][state-1] * self[state-1].getTrans()
                same = NegLog(0)
                # col-1 might not have an entry for state
                try:
                    same = forward[col-1][state] * self[state-1].getStay()
                except IndexError:
                    pass
                colList.append((change+same) * em)
            colList = colList + ([NegLog(0)]*(len(self)-len(colList)))
            forward.append(colList)
        return forward

    def expected(self):
        forward = self.forwards()
        backward = self.backwards()

        # updated to state version
        change = []
        for state in range(len(self)):
            e = NegLog(0)
            for col in range(len(self.img)):
                f = forward[col][state]
                try:
                    b = backward[col+1][state+1]
                except IndexError:
                    # no transition past last state or col
                    continue
                t = self[state].getTrans()
                e = e + f*b*t
            change.append(e)

        # updated to state version
        stay = []
        for state in range(len(self)):
            e = NegLog(0)
            for col in range(len(self.img)):
                f = forward[col][state]
                try:
                    b = backward[col+1][state]
                except IndexError:
                    # no transition past last state or col
                    continue
                t = self[state].getStay()
                e = e + f*b*t
            stay.append(e)

        mu = []
        for state in range(len(self)):
            e = NegLog(0)
            allPaths = NegLog(0)
            for col in range(len(self.img)):
                f = forward[col][state]
                b = backward[col][state]
                emit = self[state].getEmission(self.img[col])
                path = f*b/emit
                allPaths = allPaths + path
                e = e + path*NegLog(log(self.img[col]+1))
            mu.append(e/allPaths)

        trans = []
        for i in range(len(change)-1):
            trans.append(change[i]/(change[i]+stay[i]))

        for i in range(len(self)-1):
            self[i].train(trans[i], mu[i])

        # TODO
        # mu: updated mus, neglog form
        # update: updated transitions, neglog
        """
        Work out appropriate structure for training
        Handle multiple occurances of a state
        """
        return mu

    def update(self):
        for s in self.states:
            s.update()

    def train(self):
        pass
        # training
        """
        fw/bw only need probabilities and order

        training needs to referance states directly in order to update
        chars need to referance state for saving
        """


    def __getitem__(self,key):
        """Get a state by index"""
        return self.states[key]

    def __len__(self):
        return len(self.states)
