

"""
Store a model's states as referances to characters
"""

from functools import reduce

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
        """
        get current staying probability
        get advancing probability
        select
        store state

        end result: img col->state map or equivalent
            equivalent is just an odered list, which is easy
            ..use list
            ..self.fitted
        """

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
        # find the right char
        offset = 0
        while key>=len(self.chars[offset]):
            key -= len(self.chars[offset])
            offset+=1
        # get the state at offset
        return self.chars[offset][key]

    def __len__(self):
        return reduce(lambda x,y:x+len(y), self.chars, 0)
