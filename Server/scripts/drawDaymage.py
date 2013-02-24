#!/usr/bin/python

import sys, os, json, facebook, logging
from datetime import date, timedelta
import odol
from odol.Sensor import Sensor

logger = logging.getLogger('odol.drawDaymage')

"""
Started by cron every night 10 minutes past midnight:
10 0 * * * cd /home/pi/rgbc-0.2/scripts && ./drawDaymage.py
"""
def createImage(logfile, width=1440):
	global logger
	import Image, ImageDraw, time
	from datetime import tzinfo, datetime
	from math import floor
	import numpy as np

	imagefile = odol.config.get('data', 'img_path') + "/" + os.path.basename(logfile) + ".png"
	if os.path.exists(imagefile):
		logger.warn(imagefile + " already exists")
		return None
	
	logger.info("Creating image from", logfile)
	
	im = Image.new('RGBA', (width, 100), (0, 0, 0, 0))
	draw = ImageDraw.Draw(im)
	xp, fp = [], []
	
	# 2013-02-15 00:12:47,598
	for column, data in enumerate(Sensor.load_logfile(logfile)):
		d = datetime.strptime("1970-01-01 "+data[0][:8], "%Y-%m-%d %H:%M:%S")
		ts = int(time.mktime(d.timetuple()))
		xp.append(ts)
		fp.append(list(data[1]))

	nfp = np.array(fp)
	x = np.linspace(0, 86400, num=width)

	# Wertebereucgt ist 86400, 1440 werte werden gebraucht, im 60 abstand
	r =  np.interp(x, xp, nfp[:,0])
	g =  np.interp(x, xp, nfp[:,1])
	b =  np.interp(x, xp, nfp[:,2])
	c =  np.interp(x, xp, nfp[:,3])
	
	for i in range(len(x)):
		draw.line((i, 0, i, 100), fill=(int(r[i]),int(g[i]),int(b[i])))
		
	imagefile = odol.config.get('data', 'img_path') + "/" + os.path.basename(logfile) + ".png"
	im.save(imagefile, "PNG")
	return imagefile


yesterday = date.today() - timedelta(days=1)
log_suffix = odol.config.get('data', 'log_suffix')
logfile = odol.config.get('data', 'data_path') + "/odol.Sensor.log." + yesterday.strftime(log_suffix)

# Bild wird nicht gespeichert, wo es gesucht wird
if os.path.exists(logfile):
	imglocation = createImage(logfile)
	if imglocation == None:
		sys.exit()
		
else:
	logger.error("Logfile is missing:", logfile)
	sys.exit()

token = odol.config.get('facebook', 'token')
page_id = odol.config.get('facebook', 'odol_page_id')

graph = facebook.GraphAPI(token)
accounts = graph.get_connections("me", "accounts")
for account in accounts['data']:
	if account['id'] == page_id:
		graph = facebook.GraphAPI(account['access_token'])
		graph.put_photo(open(imglocation), yesterday.strftime("%A, %B %d"), page_id)	
