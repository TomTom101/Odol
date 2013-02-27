import odol
import os, logging
import Image, ImageDraw, time
from datetime import tzinfo, datetime
from math import floor
import numpy as np

def new(datafile, width=1440, height=445):
	return Draw(datafile, width, height)
	
class Draw():
	def __init__(self, datafile, width, height):
		self.logger = logging.getLogger(__name__)
		self.imagefile = odol.config.get('data', 'img_path') + "/" + os.path.basename(datafile) + ".png"
		self.datafile = datafile
		self.width = width
		self.height = height
		
	def imageExists(self):
		return os.path.exists(self.imagefile)
		
	def createImage(self):

		self.logger.info("Creating image from " + self.datafile)
	
		im = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
		draw = ImageDraw.Draw(im)
		xp, fp = [], []
		# 2013-02-15 00:12:47,598
		for column, data in enumerate(odol.Sensor.Sensor.load_logfile(self.datafile)):
			d = datetime.strptime("1970-01-01 "+data[0][:8], "%Y-%m-%d %H:%M:%S")
			ts = int(time.mktime(d.timetuple()))
			xp.append(ts)
			fp.append(list(data[1]))

		nfp = np.array(fp)

		# Wertebereich ist 86400, 1440 werte werden gebraucht, im 60 abstand
		x = np.linspace(0, 86400, num=self.width)
		r =  np.interp(x, xp, nfp[:,0])
		g =  np.interp(x, xp, nfp[:,1])
		b =  np.interp(x, xp, nfp[:,2])
		c =  np.interp(x, xp, nfp[:,3]) # not used so far
	
		for i in range(len(x)):
			draw.line((i, 0, i, self.height), fill=(int(r[i]),int(g[i]),int(b[i])))
		
		im.save(self.imagefile, "PNG")
		return self.imagefile