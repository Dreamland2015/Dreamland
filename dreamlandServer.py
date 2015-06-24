import zmq
import time
from random import randrange
from multiprocessing import Process

recv_port = '5559'
send_port = '5560'

context = zmq.Context()


def sendMessageToClients():
	send_zmq = context.socket(zmq.PUB)
	send_zmq.setsockopt(zmq.SNDHWM, 2)
	send_zmq.bind('tcp://*:' + send_port)

	message = 'hello world'
	while True:
		topic = randrange(4, 10)
		print('Sending ' + str(topic))
		send_zmq.send_string('%i, %s' % (topic, message))
		time.sleep(1)


def receiveMessageFromClients():
	# topicFilter = '9'

	zmq_recv = context.socket(zmq.SUB)
	zmq_recv.setsockopt(zmq.RCVHWM, 2)
	zmq_recv.bind('tcp://*:' + recv_port)
	zmq_recv.setsockopt_string(zmq.SUBSCRIBE, "")
	counter = 1
	while True:
		stringRecv = zmq_recv.recv_string()
		structureName, messageRecv = stringRecv.split(',')
		print('Received : ' + messageRecv + ' from ' + structureName)
		counter += 1

if __name__ == '__main__':
	Process(target=sendMessageToClients).start()
	Process(target=receiveMessageFromClients).start()
