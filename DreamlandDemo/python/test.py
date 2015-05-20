import zmq
import time
import sys
from random import randrange
from multiprocessing import Process

port_1 = '5559'
port_2 = '5560'

if sys.argv[1] == '-server':
	recv_port = port_1
	send_port = port_2
elif sys.argv[1] == '-structure':
	recv_port = port_2
	send_port = port_1
	objectName = sys.argv[2]
	serverIp = sys.argv[3]


context = zmq.Context()


def send_zmq():
	send_zmq = context.socket(zmq.PUB)
	send_zmq.bind('tcp://*:' + send_port)

	message = 'hello world'
	while True:
		topic = randrange(4, 10)
		print('Sending ' + str(topic))
		send_zmq.send_string('%i, %s' % (topic, message))
		time.sleep(1)


def recv_zmq():
	topicFilter = '9'

	zmq_recv = context.socket(zmq.SUB)
	zmq_recv.bind('tcp://*:' + recv_port)
	zmq_recv.setsockopt_string(zmq.SUBSCRIBE, topicFilter)

	counter = 1
	while True:
		stringRecv = zmq_recv.recv_string()
		topic, messageRecv = stringRecv.split(',')
		print('Received : ' + messageRecv + ' ' + str(counter) + ' times')
		counter += 1


if __name__ == '__main__':
	Process(target=send_zmq).start()
	Process(target=recv_zmq).start()
