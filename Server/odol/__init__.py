import os
import logging.handlers
import ConfigParser

__all__ = ['Sensor', 'Cosm', 'Draw']
__authors__ = "Thomas Brandl"
__license__ = "GPLv3"
__versioninfo__ = (0, 0, 2)
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
fh.setLevel(logging.INFO)	
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)

config = ConfigParser.ConfigParser()
config_file = __name__ + '.cfg'
def_config_path = os.path.join(os.path.dirname(__file__), config_file)
config_path = os.path.join(os.path.expanduser("~/odol"), config_file)

config.readfp(open(def_config_path))
config.set('data', 'home_path', os.path.expanduser("~"))
config.read(config_path)