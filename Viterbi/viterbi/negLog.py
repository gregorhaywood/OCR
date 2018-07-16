
import sys
from math import log, exp

# maximum float value represents 0
_ZERO = sys.float_info[0]
# neglog of minimum float
_PREC = -log(sys.float_info[3])-log(3)


class NegLog(object):
    def __init__(self, p=0, negLog=None):
        if negLog is not None:
            self._val = negLog
        elif p>0:
            self._val = -log(p)
        else:
            self._val = _ZERO

    def prob(self):
        if self._val == _ZERO:
            return 0
        return exp(-self._val)

    def __mul__(self,other):
        if self.isZero() or other.isZero():
            return NegLog(0)
        else:
            return NegLog(negLog=(self._val+other._val))

    def __truediv__(self,other):
        if other.isZero():
            raise ZeroDivisionError()
        elif self.isZero():
            return self.clone()
        else:
            return NegLog(negLog=(self._val-other._val))

    def __add__(self, other):
        if other.isZero() or other._val-self._val>_PREC:
            return self.clone()
        elif self.isZero() or self._val-other._val>_PREC:
            return other.clone()
        else:
            a = self._val
            b = other._val
            mn = min(a,b)
            mx = max(a,b)
            return NegLog(negLog=(-log(1+exp(mn-mx))+mn))

    def __sub__(self,other):
        if other.isZero() or other._val-self._val>_PREC:
            return self.clone()
        if other > self:
            raise ValueError("Cannot represent negative numbers in negaltive log form.")
        else:
            a = self._val
            b = other._val
            mn = min(a,b)
            mx = max(a,b)
            return NegLog(negLog=(-log(1-exp(mn-mx))+mn))

    def __lt__(self, other):
        return self._val > other._val

    def __gt__(self, other):
        return self._val < other._val

    def __str__(self):
        return str(self._val)

    def __repr__(self):
        return str(self._val)

    def clone(self):
        return NegLog(negLog=self._val)

    def isZero(self):
        return self._val == _ZERO
