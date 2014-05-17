import os

import plugins

from utils import directory
from plugins._docopt import get_help


# @TODO: Error-checking! Does directory exist? spaces in directory name?
def cd(shell, args):
	'''Change the current working directory.

Usage:
  cd [<dir>]
'''
	path = args['<dir>'] if args['<dir>'] else os.path.expanduser('~')
	with directory(shell.current_directory):
		try:
			os.chdir(path)
			shell.current_directory = os.getcwd()
		except OSError, e:
			shell.err('{} is not a valid directory!'.format(path))


def help(shell, args):
	'''Get help for a specified command.

Usage:
  help <command>
'''
	plugin = plugins.get_plugin(args['<command>'])
	if plugin:
		shell.out(get_help(plugin.__doc__))
	else:
		shell.err('"{}" is not a recognized command!'.format(args['<command>']))


def history(shell, args):
	'''Display command history.

Usage:
  history
'''
	shell.out('You typed history')


def pwd(shell, args):
	'''Print the current working directory.

Usage:
  pwd
'''
	shell.out(shell.current_directory)


# @TODO: This is ABSOLUTELY HORRIBLE. Commands should have context, not the shell (_clients is a hack)
def username(shell, args):
	'''Display or change the current username.

Usage:
  username [<new>]
'''
	if args['<new>']:
		shell._clients[shell._caller] = args['<new>']
		shell._property_update('username', args['<new>'], [shell._caller])
	else:
		shell.out(shell._clients[shell._caller])