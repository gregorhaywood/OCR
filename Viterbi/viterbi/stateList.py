

"""
Store a model's states as referances to characters
"""

from functools import reduce
from viterbi.negLog import NegLog
from math import log

SEARCH_SPACE = 0.2

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
        # TODO
        # clean up - don't need to store anything except previous column
        
        forward = []
        forward.append([(self[0].getEmission(self.img[0]), [0])]
                    + [(NegLog(0), None)]*(len(self)-1))
        # other cols
        for col in range(1,len(self.img)):
            # state is at most col
            # there is a lower limit on state as well
            # TODO 
            # will garuntee reaching end state 
            # limit is
            # len(stateList) - (len(colList)-col)
            # min 0
            
            
            # remaining columns:
            remaining = len(self.img)-col-1
            # there can be a state transition in each col of remaining
            # so only the last $remaining states can occur
            firstState = len(self)-remaining-1
            if firstState < 0:
                firstState = 0    
            colList = [(NegLog(0), None)]*firstState
            for state in range(firstState, col+1):
                try:
                    em = self[state].getEmission(self.img[col])
                except IndexError:
                    continue

                # trim search space
                if state/len(self) < col/len(self.img)-SEARCH_SPACE:
                    colList.append((NegLog(0), None))
                    continue
                if state/len(self) > col/len(self.img)+SEARCH_SPACE:
                    colList.append((NegLog(0), None))
                    continue
                
                change = NegLog(0)
                if state > 0:
                    change = forward[col-1][state-1][0] * self[state-1].getTrans()
                same = NegLog(0)
                # col-1 might not have an entry for state
                try:
                    same = forward[col-1][state][0] * self[state-1].getStay()
                except IndexError:
                    pass
                    
                # maximisation
                if same>change:
                    colList.append(((same * em), forward[col-1][state][1]))
                else:
                    colList.append(((change * em), forward[col-1][state-1][1] + [col]))
                    
            colList = colList + ([(NegLog(0), None)]*(len(self)-len(colList)))
            forward.append(colList)
        p, transCols = max(forward[-1], key=lambda x:x[0])
        
        # for each transition columns
        index = -1
        self.fitted = []
        
        for c in range(len(self.img)):
            try:
                if c < transCols[index+1]:
                    self.fitted.append(self[index])
                else:
                    index = index + 1
                    self.fitted.append(self[index])
            except IndexError:
                self.fitted.append(self[index])
        
        return self.fitted, p

    def _backwards(self):
        backward = [[]]*len(self.img)

        # col  can only be on state
        backward[-1] = [NegLog(0)]*(len(self)-1) + [self[-1].getEmission(self.img[-1])]

        # other cols
        for col in range(len(self.img)-2,-1,-1):
            # state is at most col
            colList = []
            start = len(self)-1
            end = start - (len(self.img)-col)-1
            for state in range(start, end,-1):
                if (state < 0):
                    break
                
                # trim search space
                
                if state/len(self) < col/len(self.img)-SEARCH_SPACE:
                    colList.insert(0, NegLog(0))
                    continue
                
                if state/len(self) > col/len(self.img)+SEARCH_SPACE:
                    colList.insert(0, NegLog(0))
                    continue
                    
                

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

    def _forwards(self):

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

                # trim search space
                if state/len(self) < col/len(self.img)-SEARCH_SPACE:
                    colList.append(NegLog(0))
                    continue
                if state/len(self) > col/len(self.img)+SEARCH_SPACE:
                    colList.append(NegLog(0))
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

    def train(self):
        forward = self._forwards()
        backward = self._backwards()

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
                path = f*b*emit
                allPaths = allPaths + path
                e = e + path*NegLog(log(self.img[col]+1))
            mu.append((e/allPaths).prob())

        trans = []
        for i in range(len(change)-1):
            trans.append(change[i]/(change[i]+stay[i]))


        # TODO
        # this approach is unnecessary and can be consolidated
        
        # store updates
        for i in range(len(self)-1):
            self[i].train(trans[i], mu[i])
        
        # apply changes 
        # TODO 
        for s in self.states:
            s.update()

    def __getitem__(self,key):
        """Get a state by index"""
        return self.states[key]

    def __len__(self):
        return len(self.states)
