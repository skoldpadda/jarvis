import platform


project = 'jarvis'

########################################
# Install Tasks
########################################

def install_erlang_deps_ubuntu():
	'''Ubuntu: Install Erlang dependencies'''
	deps = [
		'build-essential',
		'libncurses5-dev',
		'openssl',
		'libssl-dev',
		'fop',
		'xsltproc',
		'unixodbc-dev'
	]
	strap.run('apt-get install {}'.format(' '.join(deps)))

def install_erlang_ubuntu():
	'''Ubuntu: Install Erlang'''
	with strap.root('/usr/bin'):
		strap.run([
			'wget http://erlang.org/download/otp_src_17.1.tar.gz',
			'tar -xzvf otp_src_17.1.tar.gz'
		])
		with strap.root('otp_src_17.1'):
			strap.run('./configure').make().make('install')

def install_elixir_ubuntu():
	'''Ubuntu: Install Elixir'''
	with strap.root('/usr/bin'):
		strap.run('git clone https://github.com/elixir-lang/elixir')
		with strap.root('elixir'):
			strap.run('git checkout v1.0.0').make().make('install')

def install_phoenix_ubuntu():
	'''Ubuntu: Install Phoenix web framework'''
	# Do this relative to jarvis install directory for now
	with strap.root('..'):
		strap.run('git clone https://github.com/phoenixframework/phoenix')
		with strap.root('phoenix'):
			strap.run('git checkout v0.4.1').run('mix do deps.get, compile')

def install_client_ubuntu():
	'''Ubuntu: Install client-specific dependencies'''
	strap.run('apt-get install leiningen')

def install_ubuntu():
	'''Ubuntu-specific installation'''
	strap.run([
		install_erlang_deps_ubuntu,
		install_erlang_ubuntu,
		install_elixir_ubuntu,
		install_phoenix_ubuntu,
		install_client_ubuntu
	])

def install_orpheus():
	'''Install Orpheus, the jarvis kernel'''
	with strap.root('orpheus'):
		strap.run('mix do deps.get, compile')

def post_install():
	'''Run all post-installation tasks'''
	pass

########################################
# Run Tasks
########################################

def orpheus():
	'''Start Orpheus, the jarvis kernel'''
	with strap.root('orpheus'):
		strap.run('mix phoenix.start')

########################################
# Build Tasks
########################################

def build_client():
	with strap.root('client'):
		strap.node('gulp', module=True)

########################################
# Base Tasks
########################################

def build():
	pass

def install():
	system = platform.platform().lower()
	if 'ubuntu' in system:
		strap.run(install_ubuntu)
	strap.run(install_orpheus).run(post_install)

def default():
	strap.run(orpheus)
