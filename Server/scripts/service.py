#!/usr/bin/python

import sys, signal
from odol import *


def __exit_handler(signal, frame):
	print "Exiting ..."
	sys.exit()

signal.signal(signal.SIGINT, __exit_handler)
	
try:
	sensor = Sensor.new('/dev/bogus')
	
	while 1:
		if sensor.ser.inWaiting() > 0:
			print sensor.getData()

except (KeyboardInterrupt, SystemExit):
	sys.exit()
		
