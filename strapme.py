project = 'jarvis'


def install_erlang_deps_ubuntu():
	strap.run('apt-get install build-essential libncurses5-dev openssl libssl-dev fop xsltproc unixodbc-dev')

def install_erlang_ubuntu():
	with strap.root('/usr/bin'):
		strap.run([
			'wget http://erlang.org/download/otp_src_17.1.tar.gz',
			'tar -xzvf otp_src_17.1.tar.gz'
		])
		with strap.root('otp_src_17.1'):
			strap.run('./configure').make().make('install')

def install_elixir_ubuntu():
	with strap.root('/usr/bin'):
		strap.run('git clone https://github.com/elixir-lang/elixir')
		with strap.root('elixir'):
			strap.run('git checkout v1.0.0').make().make('install')

def install_phoenix_ubuntu():
	# Do this relative to jarvis install directory for now
	with strap.root('..'):
		strap.run('git clone https://github.com/phoenixframework/phoenix')
		with strap.root('phoenix'):
			strap.run('git checkout v0.4.1').run('mix do deps.get, compile')

def install_orpheus():
	'''Install Orpheus, the jarvis kernel'''
	with strap.root('orpheus'):
		strap.run('mix do deps.get, compile')

def post_install():
	'''Run all post-installation tasks'''
	pass

def orpheus():
	'''Start Orpheus, the jarvis kernel'''
	with strap.root('orpheus'):
		strap.run('mix phoenix.start')

def build():
	'''Build jarvis'''
	strap.node('gulp', module=True)

def install():
	strap.npm('install')

def default():
	strap.node('index.js')
