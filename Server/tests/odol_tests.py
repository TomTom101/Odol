import os, struct
from time import sleep
from nose.tools import *
from odol import *
import random

logfile = None

def setup_func():
	import odol, ConfigParser
	global logfile
	logfile = "%s/%s.log" % (odol.config.get('data', 'data_path'), Sensor.__name__)
	if os.path.exists(logfile):
		os.remove(logfile)
	
def teardown_func():
	import logging
	x = logging._handlers.copy()
	for i in x:
		log.removeHandler(i)
		i.flush()
		i.close()
	
"""
@with_setup(setup_func, teardown_func)	
def test_config():
	import odol
	assert odol.config.get('data', 'img_path') == './test_data/images'

def test_serial():
	serial_queue = ['#']
	for i in range(4):
		serial_queue.append(random.randint(0, 1023))
	assert len(serial_queue) == 5

#	dummy_serial.DEFAULT_RESPONSE = "#" + serial_queue[1:4].join('')
	#start = random.randint(1, len(serial_queue)-1)
	#print "#" + "".join(struct.pack("<h", v) for v in serial_queue[start:start+4])

	#sensor = Sensor.new('/dev/bogus')
	#dummy_serial.DEFAULT_RESPONSE = struct.pack("<chhhh", '#', 1023, 1023, 1023, 1023)
"""

@with_setup(setup_func, teardown_func)	
def test_read_log():
	import odol
	from math import ceil

	sensor = Sensor.new('/dev/bogus')
	
	i = 1
	samples = 64
	while i <= 100:
		sensor.log((int(ceil(i-1)),0,0,0))
		i+=1024/samples
		sleep(0.1)

	for column, data in enumerate(sensor.load_logfile(logfile)):
		assert data[1][0] >= 0
		assert data[1][1] == 0
		assert data[1][2] == 0
"""		
def test_create_image():
	import odol
	from scripts import drawDaymage
	img_file = createImage(os.getcwd() + "/tests/odol.Sensor_min.log")
	assert os.path.exists(img_file)
"""

def test_is_dummy():
	sensor = Sensor.new()
	assert sensor.isDummySerial() == True
	
def test_cosm():
	import threading
	import odol
	data = [10,20,300,128]
	cosm = Cosm.new()
	cosm.record(data)
	t = threading.Timer(1, cosm.record, [cosm, data], {});
	t.daemon = True
	t.start()