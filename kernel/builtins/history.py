'''Display command history.'''

def _run(args):

	@cli.cmd
	def history():
		shell.out('You typed history')

	cli.run(args, main=history)
