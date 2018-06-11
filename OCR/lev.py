#!/usr/bin/python3

# Minimum edit distance between two files, each consisting of single line.

import sys

# String edit distance.
def levenshtein(s1, s2):
	prev_row = range(len(s2) + 1)
	for i, c1 in enumerate(s1, 1):
		curr_row = [i]
		for j, c2 in enumerate(s2, 1):
			ins = prev_row[j] + 1
			dels = curr_row[j-1] + 1
			subs = prev_row[j-1] + (c1 != c2)
			curr_row.append(min(ins, dels, subs))
		prev_row = curr_row
	return prev_row[-1]

# read strings, set to empty if file does not exist
s1 = ''
s2 = ''
try:
	with open(sys.argv[1]) as f:
		s1 = f.read().strip()
except:
	s1 = ''

try:
	with open(sys.argv[2]) as f:
		s2 = f.read().strip()
except:
	s2 = ''

print(levenshtein(s1, s2), end='')
