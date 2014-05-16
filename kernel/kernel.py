import os
import shlex
import datetime

import builtins
import plugins
from plugins._docopt import docopt
from brain import brain


'''
@TODO
 - Is it better to explicitly have scripts call shell.out(), or should
   we capture/redirect stdout/stderr to allow implicit print() -ing?

 - Okay so a huge problem is everything is blocking. Should be async.
   Example: if a builtin function calls time.sleep(5) between print calls,
   it will print once, wait 5 seconds, then print again. So far so good.
   But then if the user types something else between the print calls, it gets
   buffered until the previous command finishes. MAYBE THAT'S A GOOD THING?
   Do we want users to interleave commands, or wait until each is done?
'''


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


class Directory:
	'''Context manager for changing the current working directory'''
	def __init__(self, new_path):
		self.new_path = new_path

	def __enter__(self):
		self.saved_path = os.getcwd()
		os.chdir(self.new_path)

	def __exit__(self, etype, value, traceback):
		os.chdir(self.saved_path)


class ShellException(Exception):
	pass


class Kernel(object):

	def __init__(self):
		self.direct_channel = Event()  # Call with: self.direct_channel({SOME JSON HERE})
		self._current_directory = os.path.expanduser('~')

		self._clients = {}


	'''
	The below methods encapsulate common messages sent to clients.
	They should NOT be called from outside scripts.
	'''

	def _jarvis_message(self, text):
		self.direct_channel({
			'header': {
				'type': 'jarvis_message'
			},
			'content': {
				'text': text
			}
		})

	def _property_update(self, key, value, recipients=None):
		self.direct_channel({
			'header': {
				'type': 'property_update'
			},
			'content': {
				'property': key,
				'value': value
			}
		}, recipients)


	@property
	def current_directory(self):
		return self._current_directory
	
	@current_directory.setter
	def current_directory(self, value):
		self._current_directory = value
		self._property_update('current_directory', self._current_directory)


	def out(self, text):
		self.direct_channel({
			'header': {
				'type': 'input_response'
			},
			'content': {
				'text': text
			}
		})

	def err(self, text):
		self.direct_channel({
			'header': {
				'type': 'input_response'
			},
			'content': {
				'text': text,
				'err': True
			}
		})

	def throw(self, text):
		raise ShellException(text)

	def run_command(self, command, args):

		# @TODO: Handle aliases? (preprocessing of input)

		# Is it a built-in function?
		if hasattr(builtins, command):
			f = getattr(builtins, command)
			parsed_args = docopt(f.__doc__, argv=args)
			if isinstance(parsed_args, dict):
				f(self, parsed_args)
			else:
				self.out(str(parsed_args))
			return True

		# Is it a script in the plugins/ directory?
		plugin = plugins.get_plugin(command)
		if plugin:
			try:
				parsed_args = docopt(plugin.__doc__, argv=args, version=plugin.__version__ if hasattr(plugin, '__version__') else 'No version provided')
				if isinstance(parsed_args, dict):
					plugin.run(self, parsed_args)
				else:
					self.out(str(parsed_args))
			except ShellException, e:
				self.err(str(e))
			return True



		'''
		# Is it a native shell command?
		try:
			with directory(current_directory):
				subprocess.call([command] + args)
			return
		except OSError:
			pass
		'''

		# Probably not a command, pass it to brain
		return False


	'''
	Each of the methods below handles a single type of message sent from a client.
	To broadcast a message to all connected clients, send it through self.direct_channel().
	You may also optionally return a message; this will only go to the calling client.
	'''

	def input_request(self, message):
		caller = message['header']['uid']
		self._caller = caller
		message['header']['username'] = self._clients[caller]
		self.direct_channel(message)  # Broadcast entire original message to all clients

		uin = message['content']['text']
		if not uin:
			return

		try:
			raw_cmd = shlex.split(uin)
			if self.run_command(raw_cmd[0], raw_cmd[1:]):
				return
		except ValueError:
			pass

		response = brain.receive(uin)
		if response:
			self.out(response)
			return

		# Okay...we really don't know what to do
		self.err('Sorry, I do not understand')

	def handshake_request(self, message):
		user = self._clients[message['header']['uid']]
		self._jarvis_message('{} joining on {}'.format(user, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		self.current_directory = self._current_directory  # Hack to broadcast the cd for new clients
		self._property_update('username', user, [message['header']['uid']])
		return {
			'header': {
				'username': user,
				'type': 'handshake_response'
			}
		}

	# Takes a JSON input, returns a JSON output (or nothing if it doesn't want to handle stuff)
	def handle_input(self, message):
		c = self.__class__
		msg_type = message['header']['type']
		if hasattr(c, msg_type) and callable(getattr(c, msg_type)):
			return getattr(c, msg_type)(self, message)

		# @TODO should return error (invalid message type)


	def connection_open(self, uid):
		self._clients[uid] = 'user-{}'.format(uid[:5])