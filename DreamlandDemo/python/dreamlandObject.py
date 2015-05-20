#!/usr/bin/env python
import zmq


class SendZMQ(object):
	def __init__(self, socketType):
		self.socketType = socketType
		print('socket is ' + self.socketType)
		self.setupZMQ()

	def setupZMQ(self):
		self.ctx = zmq.Context()
		self.socket = self.ctx.socket(self.socketType)
		self.socket.bind('tcp://*:5590')

	def sendMessage(self, message):
		self.socket.send_string(message)


class RecvZMQ(object):
	def __init__(self, socketType):
		self.socketType = 'zmq' + socketType
		self.setupZMQ()

	def setupZMQ(self):
		self.ctx = zmq.Context()
		self.socket = zmq.socket(self.socketType)
		self.socket.connect('tcp://localhost:5590')

	def recvMessage(self, message):
		self.socket.send_string(message)
