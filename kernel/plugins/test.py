'''Docopt testing function.

Usage:
  test ship new <name>...
  test ship <name> move <x> <y> [--speed=<kn>]
  test ship shoot <x> <y>
  test mine (set|remove) <x> <y> [--moored | --drifting]
  test (-h | --help)
  test --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
'''
from _docopt import docopt

def run(shell, args):
	arguments = docopt(__doc__, argv=args, version='Test v2.0')
	if arguments:
		shell.out(str(arguments))