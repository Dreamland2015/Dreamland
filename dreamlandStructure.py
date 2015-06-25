from multiprocessing import Process
from structureConfig import structureConfig
import time
import zmq

structureName = structureConfig["structureName"]
serverIp = 'tcp://%s:' % structureConfig["serverIp"]

recv_port = '5560'
send_port = '5559'

context = zmq.Context()

#hello world


def receiveMessageFromServer():
	topicFilter = '9'

	zmq_recv = context.socket(zmq.SUB)
	zmq_recv.setsockopt(zmq.RCVHWM, 2)
	zmq_recv.connect(serverIp + recv_port)
	zmq_recv.setsockopt_string(zmq.SUBSCRIBE, topicFilter)

	counter = 1
	while True:
		stringRecv = zmq_recv.recv_string()
		topic, messageRecv = stringRecv.split(',')
		print('Received : ' + messageRecv + ' ' + str(counter) + ' times')
		counter += 1


def sendMessageToServer():
	send_zmq = context.socket(zmq.PUB)
	send_zmq.setsockopt(zmq.SNDHWM, 2)
	send_zmq.connect(serverIp + send_port)

	message = 'hello world'
	while True:
		print('Sending ' + message)
		send_zmq.send_string('%s, %s' % (structureName, message))
		time.sleep(1)


if __name__ == '__main__':
	Process(target=receiveMessageFromServer).start()
	Process(target=sendMessageToServer).start()
