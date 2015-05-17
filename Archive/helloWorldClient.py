#!/usr/bin/env python

#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import time
import sys

sendMessage = "Hello"
context = zmq.Context()

ip = sys.argv[1]
port = 5555
string = "tcp://" + ip + ":" + str(port)

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect(string)

#  Do 10 requests, waiting each time for a response
while True:
    print("Sending request…")
    socket.send_string(sendMessage)

    #  Get the reply.
    message = socket.recv_string()
    print("Received reply [ %s ]" % message)
    time.sleep(1)
