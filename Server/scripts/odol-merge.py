#!/usr/bin/python


from odol import *
import Image
import glob

width = 400
dist = width/4
index = 0

files = glob.glob("/Users/thobra/odol/data/*.log.2013-*")

im = Image.new('RGBA', (len(files)*dist, 1440))
immask=Image.new('L', im.size, color=0)
im.putalpha(immask)
mask = Image.open("/Users/thobra/Documents/ODOL/Server/scripts/mask5-400.png.mask")


for file in files:
	draw = Draw.new(file, width=width, height=1440, mode="v")
	if (draw.imageExists()):
		imglocation = draw.imagefile
	else:
		imglocation = draw.createImage()
		
	imDay = Image.open(imglocation)
	im.paste(imDay, (dist*index, 0), mask)
	index += 1
	print imglocation

im.save("out.png")
