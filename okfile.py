project = 'jarvis'


########################################
# Install Tasks
########################################

def install_phoenix():
	'''Install Phoenix web framework'''
	# Do this relative to jarvis install directory for now
	with ok.root('..'):
		ok.run('git clone https://github.com/phoenixframework/phoenix')
		with ok.root('phoenix'):
			ok.run('git checkout v0.4.1').mix('do deps.get, compile')

def install_orpheus():
	'''Install Orpheus, the jarvis kernel'''
	with ok.root('orpheus'):
		ok.mix('do deps.get, compile')

def post_install():
	'''Run all post-installation tasks'''
	pass


########################################
# Run Tasks
########################################

def orpheus():
	'''Start Orpheus, the jarvis kernel'''
	with ok.root('orpheus'):
		ok.mix('phoenix.start')


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
	ok.run([install_phoenix, install_orpheus]).run(post_install)

def default():
	ok.run(orpheus)
