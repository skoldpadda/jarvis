import zmq

pub_port = '5556'
con_port = '5557'

context = zmq.Context()

con_socket = context.socket(zmq.REP)
con_socket.bind('tcp://127.0.0.1:{}'.format(con_port))

pub_socket = context.socket(zmq.PUB)
pub_socket.bind('tcp://127.0.0.1:{}'.format(pub_port))

while True:
	msg = con_socket.recv_pyobj()
	print 'Received request [{}]: {}'.format(msg[0], msg[1])
	con_socket.send('Request {} acknowledged'.format(msg[1]))
	pub_socket.send_pyobj(msg)