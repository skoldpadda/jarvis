import urllib
import urllib2


def receive(message):
	# @TODO: This is SO CHEAP. Just for kicks (for now)
	# Also, can use simple/json to get SOURCE and optionally IMAGES to display.
	# For example on long responses that are truncated, can add a "More" link.
	req = urllib2.Request('https://weannie.pannous.com/api', urllib.urlencode({
		'out': 'simple',
		'input': message
	}))
	response = urllib2.urlopen(req).read()
	if len(response) > 250:
		response = response[:250] + "..."
	return response