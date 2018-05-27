#!/usr/bin/python3

# String utilities.

from os import listdir
from os.path import isfile, join
from re import match, sub
import regex
import unicodedata

# Map character to hexadecimal number.
def char_to_hex(c):
	return '{:04X}'.format(ord(c))

# Map string to hexadecimal numbers separated by +.
def chars_to_hexs(s):
	return '+'.join(map(char_to_hex, s))

# Map string to Unicode names separated by +.
def chars_to_names(s):
	return ' + '.join(map(unicodedata.name, s))

# Map hexadecimal number to character.
def hex_to_char(h):
	return chr(int(h, 16))

# Map hexadecimal numbers separated by + to string.
def hexs_to_chars(hs):
	return ''.join(map(hex_to_char, hs.split('+')))

# String to list of graphemes, not including whitespace.
def str_to_graphemes(s):
	return [c for c in regex.findall(r'\X', s, regex.U) if not c.isspace()]

# File to set of graphemes, not including whitespace.
def file_to_grapheme_set(f_name):
	with open(f_name) as f:
		return set().union(*map(str_to_graphemes, f.readlines()))

# Files to set of graphemes, not including whitespace.
def files_to_grapheme_set(f_names):
	return set().union(*map(file_to_grapheme_set, f_names))

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
