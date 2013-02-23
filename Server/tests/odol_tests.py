import os
from time import sleep
from nose.tools import *
from odol import *

def test_config():
	import odol
	assert odol.config.get('data', 'img_path') == './test_data/images'
	
def test_create_Sensor():
	sensor = Sensor.new('/dev/bogus')
	i = 0
	while i < 5:
		sensor.log((2*i,i*10,i<<5,i<<6))
		i+=1
		sleep(0.1)

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