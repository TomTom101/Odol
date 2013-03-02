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
			self.ser = serial.Serial(self._port, 9600, timeout = 70) 
		except serial.SerialException, err:
			self.logger.warning("%s is unavailable, using dummy serial" % self._port)
			self.ser = dummy_serial.Serial()
			dummy_serial.DEFAULT_RESPONSE = struct.pack("<chhhh", '#', 1023, 1023, 1023, 1023)
			
	def __logger(self):
		formatter = logging.Formatter('%(asctime)s %(message)s')
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
		self.logger.log(100, Sensor.dataToString(_data))

	@staticmethod
	def dataToString(data):
		return ",".join(str(v) for v in data)
			
	@staticmethod
	def load_logfile(filename, max=255):
		import csv
		from math import ceil
		
		map_ratio = 1023.0/max

		try:
			for line in csv.reader(open(filename), delimiter=' ', skipinitialspace=True):
				try:
					yield line[1], map(lambda x: int(x)/map_ratio, line[len(line)-1].split(","))
				except:
					pass
		except (IOError):
			raise	
	
	def isDummySerial(self):
		return self.ser.__module__ == "odol.dummy_serial"
		
	def getData(self):
		data = struct.unpack("<c", self.ser.read(1))
		ctrl = data[0]
		if ctrl == "#":
			data = struct.unpack("<hhhh", self.ser.read(8))
			self.log(data)
		elif ctrl == "c":
			data = struct.unpack("<hhBBB", self.ser.read(7))
			self.logger.info("Received calibration: %s" % Sensor.dataToString(data))
		else:
			self.logger.warning("Out of synch!")
			self.synch()
			self.getData()
			
		return data

	def synch(self):
		synch_char = [0]
		self.logger.info("Synching");

		while (synch_char[0] != "#"):
			synch_char = struct.unpack("<c", self.ser.read(1))

		self.ser.read(8) # dump rest

	def calibrate(self):
		synch_char = []
		self.logger.warning("Recalibration");
		
		while (synch_char[0] != "c"):
			synch_char = struct.unpack("<c", self.ser.read(1))
			
		calibration = struct.unpack("<hhBBB", self.ser.read(7))
		self.logger.info("Received calibration: %s" % Sensor.dataToString(calibration))
