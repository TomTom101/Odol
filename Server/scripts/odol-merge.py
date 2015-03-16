#!/usr/bin/python

from odol import *
import Image, ImageFont, ImageDraw
import glob

width = 99
dist = width/3
index = 0

files = glob.glob("/Users/thobra/odol/data/*.log.2013-*")

im = Image.new('RGBA', ((len(files)+1)*dist, 1440))
immask=Image.new('L', im.size, color=0)
im.putalpha(immask)
mask = Image.open("/Users/thobra/Documents/ODOL/Server/scripts/mask-99.png.mask")
font = ImageFont.truetype("/Users/thobra/Documents/ODOL/Server/scripts/helvetica_neue_ultralight.ttf", 18)


for file in files:
	draw = Draw.new(file, width=width, height=1440, mode="v")
	if (draw.imageExists()):
		imglocation = draw.imagefile
	else:
		imglocation = draw.createImage()
		if(imglocation):
			imDay = Image.open(imglocation)
			imTxt = Image.new('RGBA', (100,20))
			imDTxt = ImageDraw.Draw(imTxt)
			imDTxt.text((0, 0), imglocation[-14:-4], font=font)
			imTxtr=imTxt.rotate(90, expand=False)
			im.paste(imDay, (dist*index, 0), mask)
			im.paste(imTxtr, (((dist*index)+50), 1200))
			index += 1

im.save(files[0][-10:] + "-" + files[-1][-10:] + ".jpg", quality=80)
