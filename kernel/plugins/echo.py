'''Display a line of text.

Usage:
  echo <string>...
'''
__version__ = '1.0'

def run(shell, args):
	shell.out(' '.join(args['<string>']))