"""
This module manages the behavior of states.
It abstracts over letters.
"""

from scipy.stats import lognorm
from math import sqrt, pi, exp, log
from viterbi.negLog import NegLog


class State(object):
    """A single state of a character's model."""

    def __init__(self, char, name, trans, mu):
        self.char = char
        self.name = name
        self.trans = trans
        self.sigma = 0.5
        self.mu = mu

    def getEmission(self, n):
        """Get the negLog representation of the emission probability"""
        a = 1/(self.sigma*sqrt(2*pi))
        b = (log(n+1)-self.mu)/self.sigma
        t = a*exp(-0.5*pow(b, 2))
        return NegLog(t)

    def __str__(self):
        return self.char + str(self.name)

    def getTrans(self): return self.trans
    def getStay(self): return NegLog(1)-self.trans

    def store(self):
        return (self.trans, self.mu)

    def train(self, trans, mu):
        try:
            self.trainTrans = self.trainTrans + trans
            self.trainMu += mu#.prob()
            self.trainCount += 1
        except AttributeError:
            self.trainCount = 1
            self.trainTrans = trans
            self.trainMu = mu#.prob()

    def update(self):
        try:
            if self.trainCount == 0: return
        except AttributeError:
            return
        tf = 0.1
        self.trans = NegLog(tf)*self.trainTrans/NegLog(self.trainCount) + NegLog(1-tf)*self.trans
        # limit domain
        #k = 0.2 # range
        #self.trans = NegLog(0.5*(1-k))+NegLog(k)*self.trans
        if self.char != " ":
            tf = 0.1
            self.mu = (tf)*self.trainMu/self.trainCount + (1-tf)*self.mu
            if self.mu < 1:
                self.mu = 1

        self.trainTrans = NegLog(0)
        self.trainMu = 0
        self.trainCount = 0


"""
Each state should have a transition probability,
an emmission probability, and a link to the next
state (or to None for the final state).

The transition probability is a float 0<x<=1
(there is always a chance of moving forwards,
and sometimes it is garunteed). It's complement
is the same state probability.

The emmission probabiility is log-normal around a
certain value. pixels is an integer 0<=x.
"""

"""
Also for each i, there is a probability distribution P(a,i,n),
where n is the number of pixels in a column in a line that are black.
...a is a character, i is the state ofset into the character
...so each state i has a P(n), where n is a pixel count


We assume P(a,i,n) is defined by a log-normal distribution, so
P(log(n) | mu,sigma) / n, for some mu and sigma, where
P(x | mu,sigma) = 1 / (sigma sqrt(2 pi)) exp(-(x-mu)^2 / 2 sigma^2) .
Let us assume that sigma is constant, while mu is determined by a and i.


"""
