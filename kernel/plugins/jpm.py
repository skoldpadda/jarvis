'''The jarvis plugin manager.'''
__version__ = '1.0'

def _run(args):
	# @TODO: Everything
	shell.out(str(args))

'''
Only standard scripts (bash replacements, etc.) should go into kernel/plugins/
If it goes in, it must also be added as an exclude in plugins/.gitignore!!!

jpm has to maintain a list of installed plugins AND THEIR VERSIONS for updating
(possibly as part of the brain key-value store?)

It grabs jarvis-plugins/registry.json for the list of available plugins.
Installing is as simple as copying from remote into kernel/plugins/
'''