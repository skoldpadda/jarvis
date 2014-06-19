'''Delay for a specified time, pause for an amount of time specified by the
sum of the values of the command line arguments.'''
import time

def _run(args):

	@cli.cmd
	@cli.cmd_arg('duration', type=float, nargs='+')
	def sleep(duration):
		time.sleep(sum(duration))
		shell.out('sleep complete')

	cli.run(args, main=sleep)
