#!/usr/bin/env python

# Import basic packages 
import os 
import sys 
import time

# Import ZeroMQ package 
import zmq 
print("Starting Pi Home Server ZeroMQ server")
# Initialize the ZeroMQ context 
context = zmq.Context()

# Configure ZeroMQ to send messages 
zmq_send = context.socket(zmq.PUB)

# The communication is made on socket 1111
zmq_send.bind("tcp://*:1111")
print "Sending messages on tcp://*:1111"

# Configure ZeroMQ to receive messages 
zmq_recv = context.socket(zmq.SUB)

# The communication is made on socket 1112
zmq_recv.bind("tcp://*:1112")
zmq_recv.setsockopt(zmq.SUBSCRIBE, '')  # subscribe to everything print "Receiving messages on tcp://*:1112"

print("Pi Home Server ZeroMQ server running !")
While True:
    message = None answer = None

    # Command to wait for an incoming message try:
        # Capture the message and store it message = zmq_recv.recv()
        print("Message received : " + message except zmq.Zmqerror as err:)
        print("The server received the following error message : " + str(err))

    # A message has been received if message:
        answer = str(int(message) * 2)
        try:
	    	print("Sending answer : " + answer zmq_send.send(answer))
        except zmq.ZMQError as err:
            print("Error while trying to send the answer : " + str(err))

# Never reached in theory ...
zmq_send.close()
zmq_recv.close()
context.term()
print("The server has been closed !")