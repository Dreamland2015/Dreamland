#!/usr/bin/env python

#   Dreamland output server
#   Binds PUB socket to tcp://*:5556
#   Publishes effect outputs to network
#

import zmq
import time


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

while True:
	dreamLandObject = "bench1"

	for number in range(10):
		socket.send_string("%s %i " % (dreamLandObject, number))
		print(str(number))
		time.sleep(1)
