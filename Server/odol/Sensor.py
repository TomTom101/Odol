#!/usr/bin/python

import odol
import os,struct
import logging
import serial
import dummy_serial as dummy_serial

def new(port=None):
	return Sensor(port)
	
class Sensor():

	def __init__(self, port):
		self.data_path = odol.config.get('data', 'data_path')
		""" init the data logger """
		self.__logger()
		self._port = port or '/dummy'
		try:
			self.ser = serial.Serial(self._port, 9600, timeout = 10) 
		except serial.SerialException, err:
			self.logger.error("%s is unavailable, using dummy serial" % self._port)
			self.ser = dummy_serial.Serial()
			dummy_serial.DEFAULT_RESPONSE = struct.pack("<chhhh", '#', 1023, 1023, 1023, 1023)
			
	def __logger(self):
		formatter = logging.Formatter('%(asctime)s #%(message)s')
		data_file = self.data_path + '/' + __name__ + '.log'
		try:
			fh = logging.handlers.TimedRotatingFileHandler(data_file, 'midnight')
		except IOError as e:
			if not os.path.exists(self.data_path):
				os.makedirs(self.data_path)
				fh = logging.handlers.TimedRotatingFileHandler(data_file, 'midnight')
			else:
				raise
					
		fh.setLevel('DATA')	
		fh.setFormatter(formatter)
		fh.suffix = odol.config.get('data', 'log_suffix')
		self.logger = logging.getLogger(__name__)
		self.logger.addHandler(fh)	
	
	def log(self, _data):
		self.logger.log(100, ",".join(str(v) for v in _data))	
	
	def isDummySerial(self):
		return self.ser.__module__ == "odol.dummy_serial"
		
	def getData(self):
		data = struct.unpack("<chhhh", self.ser.read(9))
		return data				
