from os import listdir
from os.path import isfile, join
from re import match, sub

import config

# Paths and filenames.

ocr_data_dir = config.get("DATA")

### Auxiliary

def expand_dec(page_num):
	return '{:04d}'.format(page_num)

def expand_hex(line_num):
	return '{:04x}'.format(line_num)

def extract_hex(file_name):
	return sub(r'[^0-9a-f].*', '', file_name)

def extract_hex_int(file_name):
	return int(extract_hex(file_name), 16)

def hex_sorted(names):
	return sorted(names, key=extract_hex_int)

def dir_files(d, re):
	return [f for f in listdir(d) if isfile(join(d, f)) and match(re, f)]

def dir_files_hex_sorted(d, re):
	return hex_sorted(dir_files(d, re))

### bin directory

def ocr_bin_page_image(page_num):
	return ocr_data_dir + '/bin/' + expand_dec(page_num) + '/0001.bin.png'

def ocr_bin_dir(page_num):
	return ocr_data_dir + '/bin/' + expand_dec(page_num) + '/0001'

def ocr_line_image_files(page_num):
	return dir_files_hex_sorted(ocr_bin_dir(page_num), r'.*\.bin\.png')

def ocr_trans_line_aut(page_num, line_num):
	return join(ocr_bin_dir(page_num), line_num + '.txt')

def ocr_trans_line_gold(page_num, line_num):
	return join(ocr_bin_dir(page_num), line_num + '.gt.txt')

def ocr_hocr_file(page_num):
	return ocr_data_dir + '/bin/' + expand_dec(page_num) + '/hocr.html'

### codecs directory

def ocr_codec_all():
	return ocr_data_dir + '/codecs/all.txt'

def ocr_codec_names():
	return ocr_data_dir + '/codecs/names.txt'

def ocr_codec_ordinaries():
	return ocr_data_dir + '/codecs/ordinaries.txt'

### models directory

### scan directory

def ocr_excl_file(page_num):
	return ocr_data_dir + '/scans/excl_' + expand_dec(page_num) + '.txt'

def ocr_excl(page_num):
	with open(ocr_excl_file(page_num)) as f:
		return set([l.strip() for l in f.readlines()])

### trans directory

def ocr_trans_files():
	d = ocr_data_dir + '/trans'
	return [join(d, f) for f in dir_files(d, r'trans_[0-9]+\.txt$')]

def ocr_trans_new_files():
	d = ocr_data_dir + '/trans'
	return [join(d, f) for f in dir_files(d, r'trans_[0-9]+_new\.txt$')]

def ocr_trans_file(page_num):
	return ocr_data_dir + '/trans/trans_' + expand_dec(page_num) + '.txt'

def ocr_trans_file_new(page_num):
	return ocr_data_dir + '/trans/trans_' + expand_dec(page_num) + '_new.txt'

def ocr_trans_file_boxed(page_num):
	return ocr_data_dir + '/bin/' + expand_dec(page_num) + '/boxed.xml'
