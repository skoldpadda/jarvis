import os
import glob


_plugins = {}


def load_plugin(name):
	try:
		plugin = __import__('{}.{}'.format(__name__, name), fromlist=['*'])
	except ImportError, e:
		return None
	_plugins[name] = plugin
	return plugin

def load_plugins():
	for name in glob.glob('{}/[!_]*.py'.format(os.path.dirname(os.path.abspath(__file__)))):
		load_plugin(os.path.basename(name)[:-3])

def get_plugin(name):
	if name in _plugins:
		return _plugins[name]
	return load_plugin(name)


load_plugins()