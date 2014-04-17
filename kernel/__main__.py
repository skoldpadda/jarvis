import os
import json

from tornado import ioloop, web
from sockjs.tornado import SockJSConnection, SockJSRouter

from kernel import Kernel


class IndexHandler(web.RequestHandler):
	def get(self):
		self.render('web/index.html')


# @TODO: Robustify this
# @NOTE: [message] can only be a STRING (per WebSocket protocol)
class KernelConnection(SockJSConnection):
	room = set()

	def on_open(self, info):
		# self.broadcast(self.room, 'Someone has joined.')
		self.room.add(self)

	def on_message(self, message):
		self.broadcast(self.room, message)
		response = kernel.handle_input(json.loads(message))
		if response:
			self.broadcast(self.room, json.dumps(response))

	def on_close(self):
		self.room.remove(self)
		# self.broadcast(self.room, 'Someone has left.')


if __name__ == '__main__':

	'''
	// @TODO: Load settings and user folder, if it doesn't exist make it.
    var u = path.resolve(utils.getUserHome(), 'jarvis-data');

    if (!fs.existsSync(u)) {
        fs.copySync('./js/user', u);
    }
	'''

	global kernel;
	kernel = Kernel()

	settings = {
		'static_path': os.path.join(os.path.dirname(__file__), 'web')
	}

	KernelRouter = SockJSRouter(KernelConnection, '/kernel')
	web.Application(
		[(r'/', IndexHandler)] + KernelRouter.urls,
		**settings
	).listen(8080)
	ioloop.IOLoop.instance().start()