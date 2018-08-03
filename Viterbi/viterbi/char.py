"""
This module manages the character level
abstraction over the model.
"""

from viterbi.state import State


class Char(object):

    def __init__(self, name, states):
        self.name = name
        self.states = []
        for i in range(len(states)):
            t,m = states[i]
            self.states.append(State(self.name, i, t, m))

    def __getitem__(self,key):
        return self.states[key]

    def __len__(self):
        return len(self.states)

    def store(self):
        """Get all data to store character."""
        states = list(map(lambda x: x.store(), self.states))
        return self.name, states
