import json

from tornado import ioloop, web
from sockjs.tornado import SockJSConnection, SockJSRouter

from kernel import Kernel


# @TODO: Robustify this
class KernelConnection(SockJSConnection):
	room = set()

	def on_open(self, info):
		self.broadcast(self.room, 'Someone has joined.')
		self.room.add(self)

	def on_message(self, message):
		self.broadcast(self.room, message)
		response = kernel.handle_input(json.loads(message))
		self.broadcast(self.room, json.dumps(response))

	def on_close(self):
		self.room.remove(self)
		self.broadcast(self.room, 'Someone has left.')


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

	KernelRouter = SockJSRouter(KernelConnection, '/kernel')
	web.Application(KernelRouter.urls).listen(8080)
	ioloop.IOLoop.instance().start()