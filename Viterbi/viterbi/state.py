"""
This module manages the behavior of states.
It abstracts over letters.
"""

from scipy.stats import lognorm
from math import sqrt, pi, exp, log
from viterbi.negLog import NegLog


class State(object):
    """A single state of a character's model."""

    def __init__(self, char, name, trans, mu, nextState):
        self.char = char
        self.name = name
        self.next = nextState
        # convert trans to ratio
        # 100:t
        # trans = t/(100+t)
        # trans(100+t) = t
        # 100 trans + t trans = t
        # 100 trans = (1-trans)t
        # 100 trans = (1-trans)t
        # (100 trans)/(1-trans) = t
        self.trans = trans # (100*trans)/(1-trans)
        self.sigma = 0.5
        self.mu = mu

    def _emit(self, n):
        """Get the probability of a given emission."""
        a = 1/(self.sigma*sqrt(2*pi))
        b = (log(n+1)-self.mu)/self.sigma
        t = a*exp(-0.5*pow(b, 2))
        return t

    def emission(self, n):
        """Get the negLog representation of the emission probability"""
        return NegLog(self._emit(n))

    def _getNext(self, pixels):
        """Get the next state given a starting state and pixel count."""
        if self.next is None:
            return self
        stay = self.getStay()*self.emission(pixels)
        go = self.getTrans()*self.next.emission(pixels)
        if stay>go:
            #TODO
            #print(self.char + str(self.name) + "\t" +
            #    str(pixels) + "\t" + str(self.emission(pixels)))
            return self
        else:
            #print(self.char + str(self.name) + "\t" +
            #    str(pixels) + "\t" + str(self.next.emission(pixels)))
            return self.next

    def __str__(self):
        return self.char + str(self.name)

    def toList(self):
        if self.next is None:
            return [self]
        return [self] + self.next.toList()

    def fit(self, line):
        states = [self.char+str(self.name)]
        while len(line)>1:
            line = line[1:]
            if self == self._getNext(line[0]):
                states.append(self.char+str(self.name))
            else:
                return states + self.next.fit(line)
        return states

    def getTrans(self): return (self.trans)
    def getStay(self): return NegLog(1)-self.trans

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
