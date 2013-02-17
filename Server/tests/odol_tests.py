import os
from time import sleep
from nose.tools import *
from odol import *

def test_create_Sensor():
	#print dir(odol)
	sensor = Sensor.new('/dev/bogus')
	i = 0
	while i < 10:
		sensor.log((2*i,i*10,i<<5,i<<6))
		i+=1
		sleep(0.2)

def test_is_dummy():
	sensor = Sensor.new()
	assert sensor.isDummySerial() == True