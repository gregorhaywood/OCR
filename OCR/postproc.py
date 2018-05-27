#!/usr/bin/python3

import os

from html.parser import HTMLParser
from xml.etree import cElementTree as etree
import urllib.request as urllib2

from fileutil import *
from stringutil import *

page = 1

hocr_bin_file = ocr_bin_page_image(page)
hocr_file = ocr_hocr_file(page)

fs = ocr_line_image_files(page)
for f in fs:
	h = extract_hex(f)
	trans_aut = ocr_trans_line_aut(page, h)
	with open(trans_aut, 'w') as tr:
		tr.write(h)

os.system('ocropus-hocr -o ' + hocr_file + ' ' + hocr_bin_file)

class LinksParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.tb = etree.TreeBuilder()

	def handle_starttag(self, tag, attributes):
		self.tb.start(tag, dict(attributes))

	def handle_endtag(self, tag):
		self.tb.end(tag)

	def handle_data(self, data):
		self.tb.data(data)

	def close(self):
		HTMLParser.close(self)
		return self.tb.close()

hex_to_box = {}

with open(hocr_file) as f:
	parser = LinksParser()
	parser.feed(''.join(f.readlines()))
	root = parser.close()
	for m in root.iter('span'):
		t = m.get('title')
		ts = t.split()
		if len(ts) == 5 and ts[0] == 'bbox':
			h = m.text
			hex_to_box[h] = (ts[1], ts[2], ts[3], ts[4])

outroot = etree.Element('top')
outtree = etree.ElementTree(outroot)

for f in fs:
	h = extract_hex(f)
	trans_gold = ocr_trans_line_gold(page, h)
	box = hex_to_box[h]
	with open(trans_gold) as tr:
		trans = ''.join(tr.readlines())
	child = etree.SubElement(outroot, 'line')
	child.text = trans
	child.set('xmin', box[0])
	child.set('ymin', box[1])
	child.set('xmax', box[2])
	child.set('ymax', box[3])

outtree.write(ocr_trans_file_boxed(page), encoding='UTF-8')
