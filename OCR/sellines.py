#!/usr/bin/python3

from os import listdir
from os.path import isfile, join
from re import match, sub
import unicodedata

from tkinter import *
from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage

from fileutil import ocr_excl, ocr_line_image_files, extract_hex
from fileutil import ocr_bin_dir, ocr_excl_file, hex_sorted

# Select lines.

page = 1

tk=Tk()
tk.geometry('1200x800')

##################################################

canvas = Canvas(tk, width=1100, height=800)
canvas.pack(side=LEFT)

vscroll = Scrollbar(tk, orient=VERTICAL)
vscroll.pack(side=LEFT, fill=Y)
vscroll.config(command=canvas.yview)
canvas.config(yscrollcommand=vscroll.set)

ignored = ocr_excl(page)

# Toggle line
def toggle_line(l):
	global ignored
	if l.widget.hex in ignored:
		l.widget.config(state=ACTIVE)
		ignored.remove(l.widget.hex)
	else:
		l.widget.config(state=DISABLED)
		ignored.add(l.widget.hex)

lines = Frame(canvas)
canvas.create_window(0, 0, window=lines, anchor='nw')

fs = ocr_line_image_files(page)
for f in fs:
	h = extract_hex(f)
	im = Image.open(join(ocr_bin_dir(page), f))
	(iw, ih) = im.size
	im = im.resize((int(iw/2), int(ih/2)), Image.ANTIALIAS)
	img = PhotoImage(image=im)
	lab = Label(lines, image=img)
	lab.image = img
	lab.pack()
	lab.hex = h
	if h in ignored:
		lab.config(state=DISABLED)
	lab.bind('<Button-1>', toggle_line)

def save_choices():
	with open(ocr_excl_file(page), 'w') as excl_out:
		for h in hex_sorted(ignored):
			excl_out.write(h + '\n')

saving = Button(lines, text="Save", command=save_choices)
saving.pack(side=TOP)

tk.update()
canvas.config(scrollregion=canvas.bbox("all"))

tk.mainloop()
