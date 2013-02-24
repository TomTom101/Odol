#!/usr/bin/python

import sys, signal, threading
from odol import *
from time import sleep

def __exit_handler(signal, frame):
	print "Exiting ..."
	sys.exit()

signal.signal(signal.SIGINT, __exit_handler)

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", "--port", dest="port", help="Com port to listen for data")
parser.add_option("-i", "--interval", dest="interval", type="int", default=60, help="Interval in seconds to send data")
(options, args) = parser.parse_args()

if options.port == None:
	parser.error("We need a port a least!")

try:
	sensor = Sensor.new(options.port)
	
	while 1:
		if sensor.ser.inWaiting() > 0:
			sensor.getData()

except (KeyboardInterrupt, SystemExit):
	sys.exit()
		
