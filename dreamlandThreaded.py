from structureConfig import structureConfig
import threading
import sys
import time
import zmq


# def func_to_be_threaded(functionName):
# 	threading.Thread(target=functionName).start()


class receiveMessage:
	def __init__(self, hostname, port, subscribeTo):
		self.hostname = hostname
		self.port = port
		self.subscribeTo = subscribeTo
		self.func_to_be_threaded()

	def parseIpAndPort(self):
		return 'tcp://%s:%s' % (self.hostname, self.port)

	def startZMQClient(self):
		self.context = zmq.Context()
		self.zmq_recv = self.context.socket(zmq.SUB)
		self.zmq_recv.setsockopt(zmq.RCVHWM, 1)
		self.zmq_recv.connect(self.parseIpAndPort())
		self.zmq_recv.setsockopt_string(zmq.SUBSCRIBE, self.subscribeTo)

		self.counter = 1
		while True:
			stringRecv = self.zmq_recv.recv_string()
			topic, messageRecv = stringRecv.split(',')
			print('Received : ' + messageRecv + ' ' + str(self.counter))
			self.counter += 1

	def func_to_be_threaded(self):
		threading.Thread(target=self.startZMQClient).start()


class sendMessage(receiveMessage):
	def __init__(self, hostname, port, structureName):
		self.hostname = hostname
		self.port = port
		self.structureName = structureName
		self.func_to_be_threaded()

	def startZMQClient(self):
		self.context = zmq.Context()
		self.send_zmq = self.context.socket(zmq.PUB)
		self.send_zmq.setsockopt(zmq.SNDHWM, 1)
		self.send_zmq.bind(self.parseIpAndPort())

		message = 'hello world'
		self.counter = 1
		while True:
			messageToSend = '%s, %s' % (self.structureName, message)
			print(messageToSend + ' ' + str(self.counter))
			self.send_zmq.send_string(messageToSend)
			time.sleep(.01)
			self.counter += 1


if __name__ == '__main__':
	r1 = receiveMessage('localhost', '7890', 'test')
	s1 = sendMessage('*', '7890', 'test')

	time.sleep(60)
	print('messages sent: ' + str(s1.counter))
	print('messages recv: ' + str(r1.counter))

	exit()
