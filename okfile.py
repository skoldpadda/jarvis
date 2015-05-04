project = 'jarvis'


########################################
# Install Tasks
########################################

def install_phoenix():
	'''Install Phoenix web framework'''
	ok.mix('archive.install https://github.com/phoenixframework/phoenix/releases/download/v0.12.0/phoenix_new-0.12.0.ez')

def install_orpheus():
	'''Install Orpheus, the jarvis kernel'''
	with ok.root('orpheus'):
		ok.mix('do deps.get, compile')

def install_client():
	'''Install the reference client'''
	with ok.root('client'):
		ok.npm('install').bower('install')

def post_install():
	'''Run all post-installation tasks'''
	pass


########################################
# Run Tasks
########################################

def orpheus():
	'''Start Orpheus, the jarvis kernel'''
	with ok.root('orpheus'):
		ok.mix('phoenix.server')


########################################
# Build Tasks
########################################

def build_client():
	with ok.root('client'):
		ok.node('gulp', module=True)


########################################
# Base Tasks
########################################

def build():
	pass

def install():
	ok.run([install_phoenix, install_orpheus, install_client]).run(post_install)

def default():
	ok.run(orpheus)