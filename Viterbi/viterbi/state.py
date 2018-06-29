"""
This module manages the behavior of states.
It abstracts over letters.
"""

from scipy.stats import lognorm
from math import sqrt, pi, exp

DEF_SIGMA = 1

class State(object):
    """A single state of a character's model."""

    def __init__(self, char, name, trans, mu, nextState):
        self.char = char
        self.name = name
        self.next = nextState
        self.trans = trans
        self.sigma = 1
        self.mu = mu

    def emission(self, x):
        """Get the probability of a given emission.
        This version accounts for the number of pixels
        with mu (the peak of the distribution), and
        accuracy with sigma (the deviation).
        """
        a = 1/(self.sigma*sqrt(2*pi))
        b = (x-self.mu)/self.sigma
        return a*exp(-0.5*pow(b, 2))

    def _getNext(self, x):
        """Get the next state given a starting state and pixel count."""
        if self.next is None:
            return self
        stay = (1-self.trans)*self.emission(x)
        go = self.trans*self.next.emission(x)
        if stay>go:
            return self
        else:
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
        print(self)
        return states
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
