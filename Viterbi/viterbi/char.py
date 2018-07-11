"""
This module manages the character level
abstraction over the model.
"""

from viterbi.state import State


class Char(object):

    def __init__(self, name, states):
        self.name = name
        self.states = list(states)

    def _fit(self, cols):
        """Fit the states to an input."""
        # assume first col is first state
        results = [self.state.name]
        for x in cols[1:]:
            self.state = self.state.getNext(x)
            results.append(self.state.name)
        return results

    def getStates(self, previous):
        """Add a copy of the states to the list."""
        stateMap = map(lambda x:x,self.states)
        index = 0
        if previous.next:
            t,m = next(stateMap)
            previous.next = State(self.name, index, t, m, None)
            previous = previous.next
            start = 1
            index = index + 1
        for t, m in stateMap:
            previous.next = State(self.name, index, t, m, None)
            previous = previous.next
            index = index + 1
        return previous

    def store(self):
        """Get all data to store character."""
        return self.name, self.states #list(map(lambda x,y: [x,y], self.states))
