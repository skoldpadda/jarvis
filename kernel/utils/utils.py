import os
import contextlib


# Adapted from: http://www.valuedlessons.com/2008/04/events-in-python.html
class Event:
	'''Simple event bus that manages notifying a set of handlers'''
	def __init__(self):
		self.handlers = {}

	def handle(self, handler_tuple):
		self.handlers[handler_tuple[0]] = handler_tuple[1]
		return self

	def unhandle(self, handler_id):
		self.handlers.pop(handler_id, None)
		return self

	def fire(self, message, recipients=None):
		send_to = {k: v for k, v in self.handlers.iteritems() if k in recipients} if recipients else self.handlers
		for handler in send_to.itervalues():
			handler(message)

	def get_handler_count(self):
		return len(self.handlers)

	__iadd__ = handle
	__isub__ = unhandle
	__call__ = fire
	__len__  = get_handler_count


@contextlib.contextmanager
def directory(path):
	'''Context manager for changing the current working directory'''
	if not os.path.isdir(path):
		raise Exception('"{}" is not a valid directory!'.format(path))
	prev_cwd = os.getcwd()
	os.chdir(path)
	try:
		yield
	finally:
		os.chdir(prev_cwd)