#!/usr/bin/python

import sys, os, json, facebook, logging
from datetime import date, timedelta
import odol
from odol import *
from optparse import OptionParser

parser = OptionParser()
logger = logging.getLogger('odol.odol_draw')
parser.add_option("-f", "--facebook", dest="facebook", action="store_true", help="Upload generated image to Facebook")
parser.add_option("-d", "--day", dest="day", help="Day to generate in the form yyy-mm-dd, yesterday by default")
(options, args) = parser.parse_args()

"""
Started by cron every night 10 minutes past midnight:
10 0 * * * cd /home/pi/odol-0.1/scripts && ./odol_draw.py
"""

if options.day == None:
	yesterday = date.today() - timedelta(days=1)
	log_suffix = odol.config.get('data', 'log_suffix')
	logfile = odol.config.get('data', 'data_path') + "/odol.Sensor.log." + yesterday.strftime(log_suffix)
else:
	logfile = odol.config.get('data', 'data_path') + "/odol.Sensor.log." + options.day


# Bild wird nicht gespeichert, wo es gesucht wird
if os.path.exists(logfile):
	draw = Draw.new(logfile)
	imglocation = draw.createImage()
	if imglocation == None:
		logger.error("No image was created!")
		sys.exit()	
	else:
		print imglocation	
else:
	logger.error("Logfile is missing:" + logfile)
	sys.exit()

if options.facebook == True:
	token = odol.config.get('facebook', 'token')
	page_id = odol.config.get('facebook', 'odol_page_id')

	graph = facebook.GraphAPI(token)
	accounts = graph.get_connections("me", "accounts")
	for account in accounts['data']:
		if account['id'] == page_id:
			graph = facebook.GraphAPI(account['access_token'])
			graph.put_photo(open(imglocation), yesterday.strftime("%A, %B %d"), page_id)
