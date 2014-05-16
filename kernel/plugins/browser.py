'''Open a browser, optionally to a specified URL or search query.

Usage:
  browser [<url>...]
'''
import webbrowser
import urllib

# @TODO: Make URL recognition more robust (like Chrome's omnibox, it can tell that amazon.com --> http://www.amazon.com)
# http://dev.chromium.org/user-experience/omnibox
# https://github.com/niklasb/vimium/blob/fuzzy/lib/completion.js

# http://stackoverflow.com/questions/827557/how-do-you-validate-a-url-with-a-regular-expression-in-python
def is_valid_url(url):
	import re
	regex = re.compile(
		r'^https?://'  # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
		r'localhost|'  # localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?'  # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	return url is not None and regex.search(url)

def run(shell, args):
	url = ' '.join(args['<url>']) if args['<url>'] else 'https://www.google.com/'
	if not is_valid_url(url):
		url = 'https://www.google.com/#q={}'.format(urllib.quote(url, ''))
	webbrowser.open(url)