'''Get help for a specified command.'''
import builtins
import plugins

def _run(args):

	@cli.cmd
	@cli.cmd_arg('command')
	def help(command):
		builtin = builtins.get_builtin(command)
		if builtin:
			shell.out(builtin.__doc__)  # @TODO
			return

		plugin = plugins.get_plugin(command)
		if plugin:
			shell.out(plugin.__doc__)  # @TODO
			return

		shell.err('"{}" is not a recognized command!'.format(command))

	cli.run(args, main=help)
