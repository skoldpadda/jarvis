import os
import shlex
import datetime

import plugins


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


# @TODO: Error-checking! Does directory exist? spaces in directory name?
def cd(shell, args):
	path = args[0] if args else os.path.expanduser('~')
	with Directory(shell.current_directory):
		try:
			os.chdir(path)
			shell.current_directory = os.getcwd()
		except OSError, e:
			shell.err('{} is not a valid directory!'.format(path))

def help(shell, args):
	shell.out('You typed help')

def history(shell, args):
	shell.out('You typed history')

def pwd(shell, args):
	shell.out(shell.current_directory)

# @TODO: This is ABSOLUTELY HORRIBLE. Commands should have context, not the shell (_clients is a hack)
def username(shell, args):
	if args:
		shell._clients[shell._caller] = args[0]
		shell._property_update('username', args[0], [shell._caller])
	else:
		shell.out(shell._clients[shell._caller])


# A dictionary of commands in this file
builtins = {
	'cd': cd,
	'help': help,
	'history': history,
	'pwd': pwd,
	'username': username
}


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

	def run_command(self, command, args):

		# @TODO: Handle aliases? (preprocessing of input)

		# Is it a built-in function? (right in this file)
		if command in builtins:
			builtins[command](self, args)
			return

		# Is it a script in the plugins/ directory?
		plugin = plugins.get_plugin(command)
		if plugin:
			plugin.run(self, args)
			return

		'''
		# Is it a native shell command?
		try:
			with directory(current_directory):
				subprocess.call([command] + args)
			return
		except OSError:
			pass

		# Pass it to semantic analyzer (part of conversation, etc.)
		'''

		# Okay...we really don't know what to do
		self.err('Unrecognized command "{}"'.format(command))


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

		# @TODO: This should not happen here.
		# If for example the user types "i'm doing fine" (note the quote) shlex will throw a ValueError
		raw_cmd = shlex.split(uin)

		self.run_command(raw_cmd[0], raw_cmd[1:])

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