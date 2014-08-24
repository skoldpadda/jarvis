project = 'jarvis'

def install_kernel():
	'''Install kernel'''
	with strap.root('kernel'):
		with strap.virtualenv('env'):
			strap.run([
				'pip install sockjs-tornado',
				'pip install git+https://github.com/willyg302/clip.py.git@master',
				'pip install git+https://github.com/willyg302/supers.py.git@master'
			]).freeze('requirements.txt')

def npm_root():
	'''NPM root'''
	strap.run('npm install')

def npm_nw():
	'''NPM node-webkit app'''
	with strap.root('jarvis-nw'):
		strap.run('npm install')

def kernel():
	'''Launch kernel'''
	with strap.virtualenv('kernel/env'):
		strap.run('python kernel')

def nw_app():
	'''Launch dev node-webkit app'''
	strap.run('node_modules/.bin/nodewebkit jarvis-nw')

def nw_build():
	'''Build node-webkit app'''
	strap.run('node_modules/.bin/grunt')

def install():
	strap.run([install_kernel, npm_root, npm_nw])

def default():
	strap.run(kernel)
