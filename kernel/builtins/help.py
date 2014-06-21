'''Get help for a specified command.'''
import builtins
import plugins

def _run(args):

	@cli.cmd
	@cli.cmd_arg('command')
	def help(command):
		if not shell.run_command(command, ['-h']):
			shell.err('"{}" is not a recognized command!'.format(command))

	cli.run(args, main=help)
