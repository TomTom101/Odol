import odol
import threading, logging
import eeml, eeml.datastream

def new():
	return Cosm()
	
class Cosm(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)
		self.api_key = odol.config.get('cosm', 'api_key')
		self.feed_id = odol.config.get('cosm', 'feed_id')
		self.logger = logging.getLogger(__name__)

	def record(self, data):
		try:
			_cosm = eeml.datastream.Cosm(int(self.feed_id), self.api_key)
			_cosm.update([
				eeml.Data("r", data[0]),
				eeml.Data("g", data[1]),
				eeml.Data("b", data[2]),
				eeml.Data("c", data[3])])
			_cosm.put()
		except (eeml.datastream.CosmError) as e:
			self.logger.error('CosmError: %s' % format(e))
			raise
		except StandardError as e:
			self.logger.error('StandardError: %s' % format(e))
			raise
		except:
			self.logger.error('Unexpected error: %s' % sys.exc_info()[0])
			raise