'''Display a line of text.'''
__version__ = '1.0'

def _run(args):

	@cli.cmd
	@cli.cmd_arg('words', nargs='*')
	def echo(words):
		shell.out(' '.join(words))

	cli.run(args, main=echo)
