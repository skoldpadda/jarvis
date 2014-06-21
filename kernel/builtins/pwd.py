'''Print the current working directory.'''

def _run(args):

	@cli.cmd
	def pwd():
		shell.out(shell.context['cwd'])

	cli.run(args, main=pwd)
