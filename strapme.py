project = 'jarvis'

def install_kernel():
	'''Install Kernel'''
	with strap.root('kernel'):
		with strap.virtualenv('env'):
			strap.run('pip install sockjs-tornado')
			strap.freeze('requirements.txt')

def npm_root():
	'''NPM root'''
	strap.run('npm install')

def npm_nw():
	'''NPM node-webkit app'''
	with strap.root('jarvis-nw'):
		strap.run('npm install')

def kernel():
	'''Launch Kernel'''
	with strap.virtualenv('kernel/env'):
		strap.run('python kernel')

def install():
	strap.run([install_kernel, npm_root, npm_nw])

def default():
	strap.run(kernel)
