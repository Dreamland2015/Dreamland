from config.py import structureConfig
from multiprocessing import Process
import time
import zmq

structureName = structureConfig["structureName"]
serverIp = structureConfig["serverIp"]
# serverIp = 'tcp://%s:' % sys.argv[1]
# structureName = socket.gethostname()
# print(structureName)

recv_port = '5560'
send_port = '5559'

context = zmq.Context()


def receiveMessageFromServer():
	topicFilter = '9'

	zmq_recv = context.socket(zmq.SUB)
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
	send_zmq.connect(serverIp + send_port)

	message = 'hello world'
	while True:
		print('Sending ' + message)
		send_zmq.send_string('%s, %s' % (structureName, message))
		time.sleep(1)


if __name__ == '__main__':
	Process(target=receiveMessageFromServer).start()
	Process(target=sendMessageToServer).start()
