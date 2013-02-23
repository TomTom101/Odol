import logging.handlers
import ConfigParser

__all__ = ['Sensor', 'Cosm']
__authors__ = "Thomas Brandl"
__license__ = "GPLv3"
__versioninfo__ = (0, 0, 1)
__version__ = '.'.join(map(str, __versioninfo__))


class DataFilter(logging.Filter):
	""" ignore DATA level type "errors" of levelno 100 """
	def filter(self, record):
		return record.levelno <= logging.CRITICAL
	
logging.addLevelName(100, 'DATA')
logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(__name__ + '.log')
fh.addFilter(DataFilter())
fh.setLevel(logging.WARNING)	
fh.setFormatter(formatter)
logger.addHandler(fh)


print __name__
config = ConfigParser.ConfigParser()
config.read(__name__ + '_test.cfg')
