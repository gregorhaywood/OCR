

from random import Random as Rnd

from viterbi.negLog import NegLog
from viterbi.char import Char

# for simplicity
chars = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789,.:ãẽĩõũ➽⟴⌠\&q̃ꝗꝓꝑ-"
short = ",.:⌠\-fijl1"
medium = "ABCDEFGHIJKLNOPQRSTUVXYZabcdeghkopqstuvxyz023456789ãẽĩõũ&q̃ꝗꝓꝑ"
longChar = "MWmnrw➽⟴"
# make a codex
def run():
    rnd = Rnd()
    codec = {}
    for c in chars:
        if c == " ":
            codec[c] = Char(c, [(NegLog(0.5), 0)])
        elif c in longChar:
            states = []
            for i in range(6):
                tr = rnd.randrange(25,75)/100
                mu = rnd.randrange(100,500)/100
                states.append((NegLog(tr),mu))
            states.append((NegLog(0.5),0))
            codec[c] = Char(c, states)
        elif c in medium:
            states = []
            for i in range(4):
                tr = rnd.randrange(25,75)/100
                mu = rnd.randrange(100,500)/100
                states.append((NegLog(tr),mu))
            states.append((NegLog(0.5),0))
            codec[c] = Char(c, states)
        elif c in short:
            states = []
            for i in range(2):
                tr = rnd.randrange(25,75)/100
                mu = rnd.randrange(100,500)/100
                states.append((NegLog(tr),mu))
            states.append((NegLog(0.5),0))
            codec[c] = Char(c, states)
        return codec
