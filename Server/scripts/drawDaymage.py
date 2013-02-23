#!/usr/bin/python

import sys, os, json, facebook
from datetime import date, timedelta
import odol

"""
Started by cron every night 10 minutes past midnight:
10 0 * * * cd /home/pi/rgbc-0.2/scripts && ./drawDaymage.py
"""

yesterday = date.today() - timedelta(days=1)
# Log file path and format should be taken from rgbc.Logger
log_suffix = odol.config.get('data', 'log_suffix')
logfile = odol.config.get('data', 'data_path') + "/odol.Sensor.log." + yesterday.strftime(log_suffix)
imgfile = logfile  + ".png"

# Bild wird nicht gespeichert, wo es gesucht wird
if os.path.exists(logfile) and not os.path.exists(imgfile):
	print "creating image"
	#imglocation = rgbc.createImage(logfile)
else:
	print "nothing to do, either", logfile,
	print "is missing or image ", imgfile, "exists"
	sys.exit()

token = odol.config.get('facebook', 'token')
page_id = odol.config.get('facebook', 'odol_page_id')

graph = facebook.GraphAPI(token)
accounts = graph.get_connections("me", "accounts")
for account in accounts['data']:
	if account['id'] == page_id:
		graph = facebook.GraphAPI(account['access_token'])
		graph.put_photo(open('./scripts/lines.png'), logfile, page_id)	
