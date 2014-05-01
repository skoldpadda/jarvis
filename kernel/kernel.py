import os
import shlex
import uuid
import datetime

from tornado.template import Template

from plugins import *


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
# @TODO: Ability to single out clients
class Event:

	def __init__(self):
		self.handlers = set()

	def handle(self, handler):
		self.handlers.add(handler)
		return self

	def unhandle(self, handler):
		self.handlers.discard(handler)
		return self

	def fire(self, *args, **kwargs):
		for handler in self.handlers:
			handler(*args, **kwargs)

	def get_handler_count(self):
		return len(self.handlers)

	__iadd__ = handle
	__isub__ = unhandle
	__call__ = fire
	__len__  = get_handler_count



# https://github.com/willyg302/jarvis/blob/3e254dde64587b58c5fe9c8bcd335815dd3221b5/jarvis.py




# @TODO: Error-checking! Does directory exist? spaces in directory name? if user just types "cd", go back to home!
def cd(shell, args):
	shell.out('You typed cd')

def help(shell, args):
	shell.out('You typed help')

def history(shell, args):
	shell.out('You typed history')


# A dictionary of commands in this file
builtins = {
	'cd': cd,
	'help': help,
	'history': history,
}


# A dictionary of plugins that Jarvis knows about

'''
plugins = {}

def load_plugin(name):
	try:
		#plugin = __import__('plugins.{}'.format(name), fromlist=['plugins'])
		plugin = __import__('kernel.plugins', fromlist=[name])
	except ImportError, e:
		print e
		return None
	plugins[name] = plugin
	return plugin

def populate_plugins():
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	for f in os.listdir('plugins'):
		if f.endswith('.py') and not '__init__' in f and not f.startswith('_'):
			load_plugin(f[:-3])
'''



'''
IPYTHON
{
  # The message header contains a pair of unique identifiers for the
  # originating session and the actual message id, in addition to the
  # username for the process that generated the message.  This is useful in
  # collaborative settings where multiple users may be interacting with the
  # same kernel simultaneously, so that frontends can label the various
  # messages in a meaningful way.
  'header' : {
				'msg_id' : uuid,
				'username' : str,
				'session' : uuid,
				# All recognized message type strings are listed below.
				'msg_type' : str,
	 },

  # In a chain of messages, the header from the parent is copied so that
  # clients can track where messages come from.
  'parent_header' : dict,

  # Any metadata associated with the message.
  'metadata' : dict,

  # The actual content of the message must be a dict, whose structure
  # depends on the message type.
  'content' : dict,
}
'''


class Kernel:

	def __init__(self):
		self.direct_channel = Event()  # Call with: self.direct_channel({SOME JSON HERE})
		#populate_plugins()  # Find all plugins we know about
		

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
				# @TODO: This should happen client-side!!!!
				'text': '<span style="color:red;">{}</span>'.format(text)
			}
		})

	def run_command(self, command, args):

		# @TODO: Handle aliases? (preprocessing of input)

		if command in builtins:
			builtins[command](self, args)
			return

		

		# If it's a plugin, run it
		if hasattr(globals(), command):
			getattr(globals(), command).run(self, args)
			return

		'''
		# Attempt to pass the command off to the underlying OS
		# @TODO: Error checking! (does command exist?)
		try:
			with directory(current_directory):
				subprocess.call([command] + args)
			return
		except OSError:
			pass

		# Okay...we really don't know what to do
		print('Unrecognized command "{}"'.format(command))


		/** JS Version
		 * 1. Is it a built-in function? (right in this class)
		 * 2. Is it a script in plugins/ folder (recursive)?
		 * 3. Is it a native shell command?
		 * 4. Pass to semantic analyzer
		 */

		# @TODO:
		# 2. Attempt to pass the command off to the underlying shell. If that succeeds, return.
		# 3. Interpret command semantically. This could include conversationally, etc.
		'''

	'''
	Each of the methods below handles a single type of message sent from a client.
	To broadcast a message to all connected clients, send it through self.direct_channel().
	You may also optionally return a message; this will only go to the calling client.
	'''

	def input_request(self, message):
		self.direct_channel(message)  # Broadcast entire original message to all clients

		uin = message['content']['text']
		if not uin:
			return

		# @TODO: This should not happen here.
		# If for example the user types "i'm doing fine" (note the quote) shlex will throw a ValueError
		raw_cmd = shlex.split(uin)

		self.run_command(raw_cmd[0], raw_cmd[1:])

	def handshake_request(self, message):
		user = 'user-{}'.format(str(uuid.uuid4().fields[0])[:5])  # Random 5-digit assigned username
		self.direct_channel({
			'header': {
				'username': user,
				'type': 'jarvis_message'
			},
			'content': {
				'text': '{} joining on {}'.format(user, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			}
		})
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