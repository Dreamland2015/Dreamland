import logging
import threading
import zmq
###################################################################################################
###################################################################################################
# This file is the backbone of the communication for this project, it allows for a publisher or
# subscriber to be instantiated as a server or a device. The key difference being that the server's
# hostname/IP will always be known and therefore it will bind to the sockets presented to it. For
# the structures, will connect to the servers hostname/IP since they are allowed to float around
# the network.
###################################################################################################
###################################################################################################

logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(message)s', datefmt='%m-%d %H:%M:%S', filename='serverLogs.log')


###################################################################################################
# Creates a subscription socket that, depending on the state of isServer, will either: Connect to
# a socket and filter messages that reach the output, or bind to a socket and subscribe to all
# messages that reach it.
##################################################################################################
class Subscriber(threading.Thread):
	def __init__(self, hostname, port, subscribtionFilter, isServer=False):
		threading.Thread.__init__(self)
		self.name = 'subscriber'
		self.hostname = hostname
		self.port = port
		self.serverOrNot = isServer
		self.subscribtionFilter = subscribtionFilter
		self.start()

	# Checks to see if this instance is a server, if so it binds to the socket
	def bindOrConnect(self):
		if self.serverOrNot is True:
			self.hostname = '*'
			self.zmqObject.bind(self.parseIpAndPort())
		else:
			self.zmqObject.connect(self.parseIpAndPort())

	# Checks to see if this instance is a server, if so it subscribes to everything
	def subcribeTo(self):
		if self.serverOrNot is True:
			subscribtion = ""
		else:
			subscribtion = self.subscribtionFilter

		self.zmqObject.setsockopt_string(zmq.SUBSCRIBE, subscribtion)

	# Parses the hostname and port into the string required by zmq
	def parseIpAndPort(self):
		return 'tcp://%s:%s' % (self.hostname, self.port)

	# Called to start listening on the socket for messages
	def recvMessage(self):
		stringRecv = self.zmqObject.recv_string()
		topic, publisherId, messageRecv = stringRecv.split(',')
		logging.info('Received : ' + messageRecv + ' from ' + publisherId)

		return messageRecv

	# Overrides threading.Thread's run. Allows a new thread to be created for this class instance
	def run(self):
		# setup zmq subscription socket for either a server or structure
		self.context = zmq.Context()
		self.zmqObject = self.context.socket(zmq.SUB)
		self.zmqObject.setsockopt(zmq.RCVHWM, 1)  # set the high water mark to 1, so messages are the most recent
		self.bindOrConnect()
		self.subcribeTo()

		# notify that the service has started, and start receiving commands
		logging.info('Subscriber started')


##################################################################################################
# Creates a publishing socket that binds to a socket and send messages with a topic filter for the
# subscriber to listen for. It inherits some simple methods from the subscriber class.
##################################################################################################
class Publisher(Subscriber):
	def __init__(self, hostname, port, publisherId, isServer=True):
		threading.Thread.__init__(self)
		self.name = 'publisher'
		self.hostname = hostname
		self.port = port
		self.publisherId = publisherId
		self.serverOrNot = isServer
		self.start()

	# Parse our the string for the publisher to send, prepending the topicFilter to the start
	def sendMessage(self, topicFilter, message):
		messageToSend = '%s, %s, %s' % (topicFilter, self.publisherId, message)
		logging.info("Sending : " + message + ' to ' + topicFilter)
		self.zmqObject.send_string(messageToSend)

	# expand the sendMessage method to send a single message to a list of topicFilters
	def sendMessageToMultiple(self, listOfTopicFilters, message):
		for topicFilter in listOfTopicFilters:
			self.sendMessage(topicFilter, message)

	# def sendMessageToType(self, )

	# Overrides threading.Thread's run. Allows a new thread to be created for this class instance
	def run(self):
		self.context = zmq.Context()
		self.zmqObject = self.context.socket(zmq.PUB)
		self.zmqObject.setsockopt(zmq.SNDHWM, 1)
		self.bindOrConnect()
		logging.info('Publisher started')
