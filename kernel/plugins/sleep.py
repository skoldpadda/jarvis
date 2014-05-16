'''Delay for a specified time, pause for an amount of time specified by the
sum of the values of the command line arguments.

Usage:
  sleep <time>...
'''
import time

def run(shell, args):
	try:
		durations = [float(duration) for duration in args['<time>']]
	except ValueError:
		shell.throw('Durations must be a number')
	time.sleep(sum(durations))
	shell.out('sleep complete')