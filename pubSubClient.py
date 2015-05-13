#!/usr/bin/env python

#   Dreamland output client
#   Connects SUB socket to tcp://localhost:5556
#   Collects various effect outputs

import sys
import zmq

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

ip = "localhost"
port = 5556
string = "tcp://" + ip + ":" + str(port)

print("Connecting to Dreamland server…")
socket.connect(string)
print(string)

# Subscribe to object of Dreamland (carosuel, bench, lightpost, ect...)
dreamLandObject = sys.argv[1] if len(sys.argv) > 1 else "You forgot to add the object!"
socket.setsockopt_string(zmq.SUBSCRIBE, dreamLandObject)
print("Subscribed to %s" % dreamLandObject)

while True:
	string = socket.recv_string()
	subcribedObject, number = string.split()
	print("Recieved: %s" % number)
