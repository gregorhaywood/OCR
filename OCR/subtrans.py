#!/usr/bin/python3

import sys
from os import listdir, remove
from os.path import isfile, join
from re import match
import regex

from fileutil import ocr_trans_new_files, ocr_trans_file, ocr_trans_file_new
from stringutil import hexs_to_chars

# Globally in one page substitute one grapheme for another.
# E.g. subs 4 0070+0303 0404

p_first = int(sys.argv[1])
p_last = int(sys.argv[2])
g_old = sys.argv[3]
g_new = sys.argv[4]

confirmed = len(sys.argv) == 6 and sys.argv[5] == 'confirm'

s_old = hexs_to_chars(g_old)
s_new = hexs_to_chars(g_new)

for f in ocr_trans_new_files():
	remove(f)

if s_old != '' and s_new != '':
	for p in range(p_first, p_last + 1):
		f_old = ocr_trans_file(p)
		if confirmed:
			f_new = ocr_trans_file(p)
		else:
			f_new = ocr_trans_file_new(p)

		lines = []
		with open(f_old) as f:
			lines = f.readlines()

		occurs = 0
		for line in lines:
			if line.find(s_old) >= 0:
				occurs += 1

		if occurs > 0:
			print(str(occurs) + ' occurrences in ' + f_new)
			with open(f_new, 'w') as f:
				for line in lines:
					f.write(line.replace(s_old, s_new))
