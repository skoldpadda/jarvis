import os
import glob


_builtins = {}


def load_builtin(name):
	try:
		builtin = __import__('{}.{}'.format(__name__, name), fromlist=['*'])
	except ImportError, e:
		return None
	_builtins[name] = builtin
	return builtin

def load_builtins():
	for name in glob.glob('{}/[!_]*.py'.format(os.path.dirname(os.path.abspath(__file__)))):
		load_builtin(os.path.basename(name)[:-3])

def get_builtin(name):
	if name in _builtins:
		return _builtins[name]
	return load_builtin(name)


load_builtins()