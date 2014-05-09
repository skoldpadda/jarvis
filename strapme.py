config = {
	'project': 'jarvis',
	'tasks': {
		'install_kernel': {
			'name': 'Install Kernel',
			'root': 'kernel',
			'virtualenv': 'env',
			'run': ['pip install sockjs-tornado'],
			'freeze': 'requirements.txt'
		},
		'npm_root': {
			'name': 'NPM root',
			'run': ['npm install']
		},
		'npm_nw': {
			'name': 'NPM node-webkit app',
			'root': 'jarvis-nw',
			'run': ['npm install']
		},
		'kernel': {
			'name': 'Launch Kernel',
			'virtualenv': 'kernel/env',
			'run': ['python kernel']
		},
		'install': {
			'run': ['install_kernel', 'npm_root', 'npm_nw']
		},
		'default': {
			'run': ['kernel']
		}
	}
}