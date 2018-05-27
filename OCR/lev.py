#!/usr/bin/python3

# Minimum edit distance between two files, each consisting of single line.

import sys

from stringutil import *

s1 = ''
s2 = ''
with open(sys.argv[1]) as f:
	s1 = f.read().strip()
with open(sys.argv[2]) as f:
	s2 = f.read().strip()

print(levenshtein(s1, s2), end='')
