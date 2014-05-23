import os
import shlex
import datetime

import builtins
import plugins

from utils.utils import Event
from utils.docopt import docopt
from utils.supers import *
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


class ShellException(Exception):
	pass


class Kernel(object):

	def __init__(self):
		self.direct_channel = Event()  # Call with: self.direct_channel({SOME JSON HERE}, [optional list of recipients])

		self.context = watch({
			'cwd': os.path.expanduser('~'),
			'clients': {}
		}, self.context_change)

	def context_change(self, record):
		if record['name'] == 'cwd':
			self._property_update('current_directory', self.context['cwd'])


	'''
	The below methods encapsulate common messages sent to clients.
	They should NOT be called from outside scripts.
	'''

	def _direct_message(self, type, content, recipients=None):
		message = {
			'header': {
				'type': type
			},
			'content': content
		}
		self.direct_channel(message, recipients)

	def _jarvis_message(self, text):
		self._direct_message('jarvis_message', {'text': text})

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

	def parse_command(self, f, docopt_args):
		parsed_args = docopt(**docopt_args)
		if isinstance(parsed_args, dict):
			f(self, parsed_args)
		else:
			self.out(str(parsed_args))


	def run_command(self, command, args):

		# @TODO: Handle aliases? (preprocessing of input)

		# Is it a built-in function?
		if hasattr(builtins, command):
			f = getattr(builtins, command)
			self.parse_command(f, {
				'doc': f.__doc__,
				'argv': args
			})
			return True

		# Is it a script in the plugins/ directory?
		plugin = plugins.get_plugin(command)
		if plugin:
			try:
				self.parse_command(plugin.run, {
					'doc': plugin.__doc__,
					'argv': args,
					'version': plugin.__version__ if hasattr(plugin, '__version__') else 'No version provided'
				})
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
		message['header']['username'] = self.context['clients'][caller]
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
		user = self.context['clients'][message['header']['uid']]
		self._jarvis_message('{} joining on {}'.format(user, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		self.context['cwd'] = self.context['cwd']  # Hack to broadcast the cd for new clients
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
		self.context['clients'][uid] = 'user-{}'.format(uid[:5])