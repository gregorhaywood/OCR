#!/usr/bin/env python3

# Gather all characters occurring in transcriptions.

from os import listdir
from os.path import isfile, join
from re import match
import regex
import unicodedata

from fileutil import ocr_trans_files, ocr_codec_all, ocr_codec_names
from stringutil import files_to_grapheme_set, chars_to_hexs, chars_to_names

cs = sorted(files_to_grapheme_set(ocr_trans_files()))

with open(ocr_codec_all(), 'w') as f:
	f.write(''.join(cs) + '\n')

with open(ocr_codec_names(), 'w') as f:
	for c in cs:
		f.write(c + '\t' + chars_to_hexs(c) + '\t' + chars_to_names(c) + '\n')
