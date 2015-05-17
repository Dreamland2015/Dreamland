#!/usr/bin/env python

#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import time

sendMessage = b"Hello"
context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.2.3:5555")

#  Do 10 requests, waiting each time for a response
while True:
    print("Sending request…")
    socket.send(sendMessage)

    #  Get the reply.
    message = socket.recv()
    print("Received reply [ %s ]" % message.decode())
    time.sleep(1)
