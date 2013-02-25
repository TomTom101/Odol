#!/usr/bin/python

import sys, os, json, facebook, logging
from datetime import date, timedelta
import odol
from odol import *

logger = logging.getLogger('odol.odol_draw')

"""
Started by cron every night 10 minutes past midnight:
10 0 * * * cd /home/pi/odol-0.1/scripts && ./odol_draw.py
"""

yesterday = date.today() - timedelta(days=1)
log_suffix = odol.config.get('data', 'log_suffix')
logfile = odol.config.get('data', 'data_path') + "/odol.Sensor.log." + yesterday.strftime(log_suffix)

# Bild wird nicht gespeichert, wo es gesucht wird
if os.path.exists(logfile):
	draw = Draw.new(logfile)
	imglocation = draw.createImage()
	if imglocation == None:
		sys.exit()		
else:
	logger.error("Logfile is missing:" + logfile)
	sys.exit()

token = odol.config.get('facebook', 'token')
page_id = odol.config.get('facebook', 'odol_page_id')

graph = facebook.GraphAPI(token)
accounts = graph.get_connections("me", "accounts")
for account in accounts['data']:
	if account['id'] == page_id:
		graph = facebook.GraphAPI(account['access_token'])
		graph.put_photo(open(imglocation), yesterday.strftime("%A, %B %d"), page_id)	
