from tornado import ioloop, web

from sockjs.tornado import SockJSConnection, SockJSRouter


class KernelConnection(SockJSConnection):
	participants = set()

	def on_open(self, info):
		self.broadcast(self.participants, 'Someone has joined.')
		self.participants.add(self)

	def on_message(self, message):
		self.broadcast(self.participants, message)

	def on_close(self):
		self.participants.remove(self)
		self.broadcast(self.participants, 'Someone has left.')


if __name__ == '__main__':
	KernelRouter = SockJSRouter(KernelConnection, '/kernel')
	web.Application(KernelRouter.urls).listen(8080)
	ioloop.IOLoop.instance().start()