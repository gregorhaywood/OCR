"""This package implements OCR with a Markov model.

The package implements the model, which uses a chain of models
for each character, as well as algorithms for training and use.

This is an unfinished prototype.
This branch implements a new state list abstration.

"""

__version__ = '0.2 In Development'

from viterbi.state import State
from viterbi.char import Char
from viterbi.negLog import NegLog
from viterbi.model import Model
