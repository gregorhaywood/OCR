#!/usr/bin/python3

import sys
from os.path import isfile

from fileutil import *

# Split up file with transcriptions into separate lines.
# If the file doesn't exist, make file with empty lines.

page = int(sys.argv[1])

def init_trans(page):
	if not isfile(ocr_trans_file(page)):
		with open(ocr_trans_file(page), 'w') as f:
			for _ in ocr_line_image_files(page):
				f.write('\n')

init_trans(page)

def split_trans(page):
	with open(ocr_trans_file(page)) as f_in:
		for i, line in enumerate(f_in.readlines(), 1):
			h = '01' + expand_hex(i)
			with open(ocr_trans_line_gold(page, h), 'w') as f_out:
				f_out.write(line)

split_trans(page)
