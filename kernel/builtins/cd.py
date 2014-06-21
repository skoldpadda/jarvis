'''Change the current working directory.'''
import os
from lib.utils import directory

# @TODO: Error-checking! Does directory exist? spaces in directory name?
def _run(args):

	@cli.cmd
	@cli.cmd_arg('path', default=os.path.expanduser('~'))
	def cd(path):
		with directory(shell.context['cwd']):
			try:
				os.chdir(path)
				shell.context['cwd'] = os.getcwd()
			except OSError, e:
				shell.err('{} is not a valid directory!'.format(path))

	cli.run(args, main=cd)
