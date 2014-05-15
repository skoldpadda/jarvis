import time

def run(shell, args):
	if not args:
		shell.err('You must provide a duration')
		return
	try:
		duration = float(args[0])
	except ValueError:
		shell.err('Duration must be a number')
		return
	time.sleep(duration)
	shell.out('sleep complete')