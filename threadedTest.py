# from structureConfig import structureConfig
import threading
# import sys
import time
import zmq


class Subscriber(threading.Thread):
	def __init__(self, hostname, port, subscribtionFilter, isServer=False):
		threading.Thread.__init__(self)
		self.name = 'subscriber'
		self.hostname = hostname
		self.port = port
		self.serverOrNot = isServer
		self.subscribtionFilter = subscribtionFilter
		self.start()

	def bindOrConnect(self):
		if self.serverOrNot is True:
			self.hostname = '*'
			self.zmqObject.bind(self.parseIpAndPort())
		else:
			self.zmqObject.connect(self.parseIpAndPort())

	def subcribeTo(self):
		if self.serverOrNot is True:
			subscribtion = ""
		else:
			subscribtion = self.subscribtionFilter
		self.zmqObject.setsockopt_string(zmq.SUBSCRIBE, subscribtion)

	def parseIpAndPort(self):
		return 'tcp://%s:%s' % (self.hostname, self.port)

	def recvMessage(self):
		while True:
			stringRecv = self.zmqObject.recv_string()
			topic, messageRecv = stringRecv.split(',')
			print('Received : ' + messageRecv + ' from ' + topic)

	def run(self):
		self.context = zmq.Context()
		self.zmqObject = self.context.socket(zmq.SUB)
		self.zmqObject.setsockopt(zmq.RCVHWM, 1)
		self.bindOrConnect()
		self.subcribeTo()
		print('Publisher started')
		self.recvMessage()


class Publisher(Subscriber):
	def __init__(self, hostname, port, isServer=True):
		threading.Thread.__init__(self)
		self.name = 'publisher'
		self.hostname = hostname
		self.port = port
		self.serverOrNot = isServer
		self.start()

	def sendMessage(self, structureName, message):
		messageToSend = '%s, %s' % (structureName, message)
		print("Sending : " + message + ' to ' + structureName)
		self.zmqObject.send_string(messageToSend)

	def sendMessageToMultiple(self, structureNames, message):
		for structureName in structureNames:
			self.sendMessage(structureName, message)

	def run(self):
		self.context = zmq.Context()
		self.zmqObject = self.context.socket(zmq.PUB)
		self.zmqObject.setsockopt(zmq.SNDHWM, 1)
		self.bindOrConnect()
		print('Subscriber started')


if __name__ == '__main__':
	r1 = Subscriber('localhost', '2345', 'carousel', False)
	r2 = Subscriber('localhost', '2345', 'bench_1', False)
	r3 = Subscriber('localhost', '2345', 'bench_2', False)
	s1 = Publisher('localhost', '2345', True)
	time.sleep(2)
	for thread in threading.enumerate():
		print(thread)

	# for x in range(1):
	# 	message = input()
	# 	topic, message = message.split(',')
	# 	print(message)
	# 	s1.sendMessage(topic, message)

	s1.sendMessageToMultiple(['carousel', 'bench_1', 'bench_2'], 'Hello World')


