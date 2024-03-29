import odol
import os, logging
import Image, ImageDraw, time
from datetime import tzinfo, datetime
from math import floor
import numpy as np

def new(datafile, width=1440, height=445, mode="h"):
	return Draw(datafile, width, height, mode)
	
class Draw():
	def __init__(self, datafile, width, height, mode):
		self.logger = logging.getLogger(__name__)
		self.imagefile = odol.config.get('data', 'img_path') + "/" + os.path.basename(datafile) + ".png"
		self.datafile = datafile
		self.width = width
		self.height = height
		self.mode = mode
		
	def imageExists(self):
		return os.path.exists(self.imagefile)
		
	@staticmethod
	def interpolate_data(data, num=1440):
		""" interpolates by default from values every second to every minutes """
		xp, fp = [], []
		for column, data in enumerate(data):
			""" 2013-03-01 07:54:46,257 r,g,b,c """
			""" first timestamp should be slightly above 0 """
			""" @todo timzone problem, first is -3556 or 3600 or 1h too small """
			d = datetime.strptime("1970-01-01 "+data[0][:8], "%Y-%m-%d %H:%M:%S")
			ts = int(time.mktime(d.timetuple())) + 3600
			xp.append(ts)
			fp.append(list(data[1]))

		nfp = np.array(fp)
		""" range is fixed and seems it must be greater than num and defines the possible resolution """
		x = np.linspace(0, 86400, num=num)
		r = np.interp(x, xp, nfp[:,0])
		g = np.interp(x, xp, nfp[:,1])
		b = np.interp(x, xp, nfp[:,2])
		c = np.interp(x, xp, nfp[:,3]) # not used so far
		
		return dict(r=r, g=g, b=b, c=c)
		
	def createImage(self):

		self.logger.info("Creating image from " + self.datafile)
	
		im = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
		draw = ImageDraw.Draw(im)
		data = Draw.interpolate_data(odol.Sensor.Sensor.load_logfile(self.datafile), self.width if self.mode == "h" else self.height)

		if(max((int(data['r'][0]) + int(data['g'][0]) + int(data['b'][0])), (int(data['r'][-1]) + int(data['g'][-1]) + int(data['b'][-1]))) > 20):
			return False
		
		for i in range(len(data['r'])):
			fill_color = fill=(int(data['r'][i]),int(data['g'][i]),int(data['b'][i]))
			if self.mode == "v":
				draw.line((0, i, self.width, i), fill=fill_color)
			else:
				draw.line((i, 0, i, self.height), fill=fill_color)
		
		im.save(self.imagefile, "PNG")
		return self.imagefile