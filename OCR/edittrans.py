#!/usr/bin/python3

from os import listdir
from os.path import isfile, join
from re import match, sub
import unicodedata

from tkinter import *
from PIL import ImageTk, Image
from PIL.ImageTk import PhotoImage

from fileutil import ocr_line_image_files, ocr_excl, extract_hex, ocr_bin_dir
from fileutil import ocr_trans_line_aut, ocr_trans_line_gold, ocr_trans_file, ocr_codec_all, ocr_codec_ordinaries
from stringutil import file_to_grapheme_set, chars_to_names

# Edit transcriptions of images, each of one line.

page = 1

tk=Tk()
tk.geometry('1800x800')

##################################################

left_canvas = Canvas(tk, width=1100, height=800)
left_canvas.pack(side=LEFT)

left_vscroll = Scrollbar(tk, orient=VERTICAL)
left_vscroll.pack(side=LEFT, fill=Y)
left_vscroll.config(command=left_canvas.yview)
left_canvas.config(yscrollcommand=left_vscroll.set)

# Record last visited entry.
last_entry_leave = None
def note_entry_pos(e):
	global last_entry_leave
	last_entry_leave = e.widget

lines = Frame(left_canvas)
left_canvas.create_window(0, 0, window=lines, anchor='nw')

file_to_entry = {}
fs = ocr_line_image_files(page)
ignored = ocr_excl(page)
for f in fs:
	h = extract_hex(f)
	if h in ignored:
		continue
	im = Image.open(join(ocr_bin_dir(page), f))
	(iw, ih) = im.size
	im = im.resize((int(iw/2), int(ih/2)), Image.ANTIALIAS)
	img = PhotoImage(image=im)
	lab = Label(lines, image=img)
	lab.image = img
	lab.pack()
	var = StringVar()
	entry = Entry(lines, textvariable=var, font = "Helvetica 20 bold", width=70)
	entry.pack()
	entry.bind('<Leave>', note_entry_pos)
	entry.textvar = var
	file_to_entry[f] = entry
	trans_aut = ocr_trans_line_aut(page, h)
	trans_gt = ocr_trans_line_gold(page, h)
	if isfile(trans_gt):
		with open(trans_gt) as intrans:
			var.set(' '.join(intrans.readlines()).strip())
	elif isfile(trans_aut):
		with open(trans_aut) as intrans:
			var.set(' '.join(intrans.readlines()).strip())
	else:
		var.set('')

def save_lines():
	with open(ocr_trans_file(page), 'w') as outf:
		for f in fs:
			h = extract_hex(f)
			if h in ignored:
				outf.write('\n')
			else:
				outf.write(file_to_entry[f].get() + '\n')

saving = Button(lines, text="Save", command=save_lines)
saving.pack(side=TOP)

tk.update()
left_canvas.config(scrollregion=left_canvas.bbox("all"))

##################################################

right_canvas = Canvas(tk, width=650, height=800)
right_canvas.pack(side=LEFT)

right_vscroll = Scrollbar(tk, orient=VERTICAL)
right_vscroll.pack(side=LEFT, fill=Y)
right_vscroll.config(command=right_canvas.yview)
right_canvas.config(yscrollcommand=right_vscroll.set)

# Is to contain hexadecimal number of character.
uvar = StringVar()

# Insert character in entry.
def insert_char(c):
	if last_entry_leave is not None:
		last_entry_leave.insert(INSERT, c)
		last_entry_leave.focus_set()
def insert_unicode():
	insert_char(hexs_to_chars(uvar.get()))

char_set = file_to_grapheme_set(ocr_codec_all())
ord_char_set = file_to_grapheme_set(ocr_codec_ordinaries())
char_set.difference_update(ord_char_set)
char_set = sorted(char_set)

chars = Frame(right_canvas)
right_canvas.create_window(0, 0, window=chars, anchor='nw')

for c in char_set:
	descr = c + ' ' + chars_to_names(c)
	but = Button(chars, text=descr, font = "Helvetica 12 bold",
			command=lambda c=c: insert_char(c))
	but.pack(side=TOP, anchor='nw')

ucode = Entry(chars, textvariable=uvar, font="Helvetica 20 bold", width=6)
ucode.pack(side=TOP)
uenter = Button(chars, text="enter Unicode", command=insert_unicode)
uenter.pack(side=TOP)

tk.update()
right_canvas.config(scrollregion=right_canvas.bbox("all"))

tk.mainloop()
