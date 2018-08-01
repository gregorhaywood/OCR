#!/usr/bin/env python3

from os.path import isfile
import argparse

from fileutil import ocr_trans_file, expand_hex, ocr_trans_line_gold

# Split up file with transcriptions into separate lines.
# If the file doesn't exist, make file with empty lines.


def init_trans(page):
	"""Initialise a transcription for a page."""
	if not isfile(ocr_trans_file(page)):
		with open(ocr_trans_file(page), 'w') as f:
			for _ in ocr_line_image_files(page):
				f.write('\n')

def split_trans(page):
	"""Make a new file for each transcription line."""
	# TODO
	# shuld be a gt for each .bin.png
	h = ""
	with open(ocr_trans_file(page)) as f_in:
		for i, line in enumerate(f_in.readlines(), 1):
			h = '01' + expand_hex(i)
			with open(ocr_trans_line_gold(page, h), 'w') as f_out:
				f_out.write(line)
				print("Written to {0}".format(ocr_trans_line_gold(page, h)))
	# add extra blank lines

def main(page):
	init_trans(page)
	split_trans(page)
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Split a transcription file into lines.")
	parser.add_argument("file", type=int, nargs="?", metavar="FILE", help="The page number of the file.")
	args = parser.parse_args()
	main(args.file)

