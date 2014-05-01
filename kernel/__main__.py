import os
import json
import signal

from tornado import ioloop, web
from sockjs.tornado import SockJSConnection, SockJSRouter

from kernel import Kernel


def add_shutdown_signal(signal_type):
	signal.signal(signal_type, lambda sig, frame: ioloop.IOLoop.instance().add_callback_from_signal(on_shutdown))

def on_shutdown():
	ioloop.IOLoop.instance().stop()


class IndexHandler(web.RequestHandler):
	def get(self):
		self.render('web/index.html')


# @TODO: Robustify this
# @NOTE: [message] can only be a STRING (per WebSocket protocol)
class KernelConnection(SockJSConnection):

	def __init__(self, session):
		super(KernelConnection, self).__init__(session)
		kernel.direct_channel += self.from_kernel

	def on_open(self, info):
		pass

	def on_message(self, message):
		response = kernel.handle_input(json.loads(message))
		if response:
			self.send(json.dumps(response))

	def on_close(self):
		pass

	def from_kernel(self, message):
		self.send(json.dumps(message))


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
	add_shutdown_signal(signal.SIGINT)
	add_shutdown_signal(signal.SIGTERM)
	ioloop.IOLoop.instance().start()