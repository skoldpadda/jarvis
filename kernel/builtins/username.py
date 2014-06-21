'''Display or change the current username.'''

# @TODO: This is ABSOLUTELY HORRIBLE. Commands should have context, not the shell (_caller is a hack)
def _run(args):

	@cli.cmd
	@cli.cmd_arg('new', nargs='?', default=None)
	def username(new):
		if new:
			shell.context['clients'][shell._caller] = new
			shell._property_update('username', new, [shell._caller])
		else:
			shell.out(shell.context['clients'][shell._caller])

	cli.run(args, main=username)