project = 'jarvis'

def build():
	'''Build jarvis'''
	strap.run('node_modules/.bin/gulp')

def install():
	strap.npm('install')

def default():
	strap.node('index.js')
